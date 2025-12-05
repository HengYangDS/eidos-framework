from typing import Iterator, Any
import json
from urllib.parse import urlparse, parse_qs
from ..system.logging import get_logger

logger = get_logger(__name__)

try:
    import redis
except ImportError:
    redis = None

class RedisConnector:
    """
    Universal Redis Adapter.
    URI Format: redis://host:6379/key?mode=list|stream|channel
    """
    
    @staticmethod
    def _connect(uri: str):
        if redis is None:
            logger.error("Redis dependency missing")
            raise ImportError("redis not installed. Run 'pip install eidos-framework[io]'")
            
        parsed = urlparse(uri)
        host = parsed.hostname or "localhost"
        port = parsed.port or 6379
        key = parsed.path.strip("/")
        params = parse_qs(parsed.query)
        mode = params.get("mode", ["list"])[0]
        
        client = redis.Redis(host=host, port=port, decode_responses=True)
        return client, key, mode

    @staticmethod
    def read(uri: str) -> Iterator[Any]:
        client, key, mode = RedisConnector._connect(uri)
        logger.info("Connecting to Redis Source", uri=uri, mode=mode)
        
        try:
            if mode == "list":
                # BLPOP logic for queue
                while True:
                    # blpop returns (key, element)
                    result = client.blpop(key, timeout=1) # Timeout 1s to allow check
                    if result:
                        try:
                            yield json.loads(result[1])
                        except json.JSONDecodeError:
                            yield {"raw": result[1]}
                    
            elif mode == "stream":
                # XREAD logic
                last_id = "$" 
                while True:
                    resp = client.xread({key: last_id}, count=1, block=1000)
                    if resp:
                        for _, messages in resp:
                            for msg_id, data in messages:
                                last_id = msg_id
                                yield data
                            
            elif mode == "channel":
                # PubSub
                pubsub = client.pubsub()
                pubsub.subscribe(key)
                for message in pubsub.listen():
                    if message["type"] == "message":
                        try:
                            yield json.loads(message["data"])
                        except json.JSONDecodeError:
                             yield {"raw": message["data"]}
        except Exception as e:
            logger.error("Redis read error", error=str(e))
            raise

    @staticmethod
    def write(uri: str, stream: Iterator[Any]) -> Iterator[Any]:
        client, key, mode = RedisConnector._connect(uri)
        logger.info("Connecting to Redis Sink", uri=uri, mode=mode)
        
        count = 0
        for item in stream:
            data = json.dumps(item)
            if mode == "list":
                client.rpush(key, data)
            elif mode == "stream":
                if isinstance(item, dict):
                    client.xadd(key, item)
                else:
                    client.xadd(key, {"data": data})
            elif mode == "channel":
                client.publish(key, data)
            
            count += 1
            yield item
            
        logger.info("Redis Sink finished", count=count)
