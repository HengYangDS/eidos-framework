from typing import Iterator, Any
import json
from urllib.parse import urlparse
from ..system.logging import get_logger

logger = get_logger(__name__)

try:
    from kafka import KafkaConsumer, KafkaProducer
except ImportError:
    KafkaConsumer = None
    KafkaProducer = None

class KafkaConnector:
    """
    Universal Kafka Adapter.
    URI Format: kafka://broker:9092/topic
    """
    
    @staticmethod
    def read(uri: str) -> Iterator[dict]:
        if KafkaConsumer is None:
            logger.error("Kafka dependency missing")
            raise ImportError("kafka-python not installed. Run 'pip install eidos-framework[io]'")
        
        parsed = urlparse(uri)
        broker = parsed.netloc
        topic = parsed.path.strip("/")
        
        logger.info("Connecting to Kafka Source", broker=broker, topic=topic)
        
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[broker],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='eidos-consumer-group',
            consumer_timeout_ms=1000 # Don't block forever in some contexts, or maybe make it configurable?
            # For infinite streams, we usually want to block. 
            # But for PythonBackend which is often used for testing/dev, maybe a timeout or manual stop is better?
            # Let's leave default (block forever) but maybe handling stop signals.
        )
        
        try:
            for message in consumer:
                yield message.value
        except Exception as e:
            logger.error("Kafka read error", error=str(e))
            raise

    @staticmethod
    def write(uri: str, stream: Iterator[Any]) -> Iterator[Any]:
        if KafkaProducer is None:
            logger.error("Kafka dependency missing")
            raise ImportError("kafka-python not installed.")
            
        parsed = urlparse(uri)
        broker = parsed.netloc
        topic = parsed.path.strip("/")
        
        logger.info("Connecting to Kafka Sink", broker=broker, topic=topic)
        
        producer = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        count = 0
        try:
            for item in stream:
                producer.send(topic, value=item)
                count += 1
                yield item
        finally:
            producer.flush()
            logger.info("Kafka Sink flushed", count=count)
