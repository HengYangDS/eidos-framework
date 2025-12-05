import unittest
from unittest.mock import MagicMock, patch
import sys

# We need to reload eidos modules to pick up patches if they were already imported
# But for a fresh test run it should be fine.

class TestIOAdapters(unittest.TestCase):
    
    def setUp(self):
        # Clear cached modules to ensure patches apply
        for mod in list(sys.modules.keys()):
            if mod.startswith("eidos.io"):
                del sys.modules[mod]

    def test_kafka_source_sink(self):
        print("\n--- Testing Kafka Adapter ---")
        
        mock_kafka = MagicMock()
        
        # Mock Consumer
        mock_consumer = MagicMock()
        mock_consumer.__iter__.return_value = [
            MagicMock(value={"id": 1, "msg": "hello"}),
            MagicMock(value={"id": 2, "msg": "world"})
        ]
        mock_kafka.KafkaConsumer.return_value = mock_consumer
        
        # Mock Producer
        mock_producer = MagicMock()
        mock_kafka.KafkaProducer.return_value = mock_producer
        
        with patch.dict(sys.modules, {'kafka': mock_kafka}):
            # Now import internal modules inside the patch context
            from eidos.io.kafka import KafkaConnector
            
            # Test Source (Read)
            # The read method yields dictionaries directly
            gen = KafkaConnector.read("kafka://broker/in-topic")
            data = list(gen)
            
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0], {"id": 1, "msg": "hello"})
            
            mock_kafka.KafkaConsumer.assert_called_with(
                "in-topic",
                bootstrap_servers=["broker"],
                value_deserializer=unittest.mock.ANY,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='eidos-consumer-group',
                consumer_timeout_ms=1000
            )
            
            # Test Sink (Write)
            # Pass the data we just read
            out_gen = KafkaConnector.write("kafka://broker/out-topic", iter(data))
            results = list(out_gen)
            
            self.assertEqual(len(results), 2)
            mock_kafka.KafkaProducer.assert_called_with(
                bootstrap_servers=["broker"],
                value_serializer=unittest.mock.ANY
            )
            self.assertEqual(mock_producer.send.call_count, 2)
            mock_producer.flush.assert_called_once()

    def test_redis_sink(self):
        print("\n--- Testing Redis Adapter ---")
        
        mock_redis = MagicMock()
        mock_client = MagicMock()
        mock_redis.Redis.return_value = mock_client
        
        with patch.dict(sys.modules, {'redis': mock_redis}):
            from eidos.io.redis import RedisConnector
            
            data = [{"val": 10}, {"val": 20}]
            
            # Test List Mode
            res = list(RedisConnector.write("redis://localhost/mylist?mode=list", iter(data)))
            self.assertEqual(len(res), 2)
            self.assertEqual(mock_client.rpush.call_count, 2)
            
            # Test Stream Mode
            mock_client.reset_mock()
            res = list(RedisConnector.write("redis://localhost/mystream?mode=stream", iter(data)))
            self.assertEqual(mock_client.xadd.call_count, 2)
            
            # Test PubSub Mode
            mock_client.reset_mock()
            res = list(RedisConnector.write("redis://localhost/mychan?mode=channel", iter(data)))
            self.assertEqual(mock_client.publish.call_count, 2)

    @patch("eidos.io.kafka.KafkaConsumer")
    def test_backend_integration(self, mock_consumer_cls):
        print("\n--- Testing PythonBackend Integration ---")
        # We can test if PythonBackend correctly delegates to KafkaConnector
        
        # Setup Mock
        mock_consumer = MagicMock()
        mock_consumer.__iter__.return_value = [MagicMock(value={"a": 1})]
        mock_consumer_cls.return_value = mock_consumer
        
        # We need to make sure kafka is present in sys.modules for the import to work
        with patch.dict(sys.modules, {'kafka': MagicMock()}):
            from eidos import Source, Sink, run
            
            # Define flow
            flow = Source("kafka://localhost/topic") >> Sink("collect")
            
            # Run
            # We must force Python backend
            execute = run(flow, engine="python")
            res = execute()
            
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0], {"a": 1})

if __name__ == "__main__":
    unittest.main()
