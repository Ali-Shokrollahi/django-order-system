from django.conf import settings
from redis import StrictRedis


redis_client = StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0, 
    decode_responses=True
)