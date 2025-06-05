import redis
from app.config import REDIS_PORT, REDIS_HOST


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
