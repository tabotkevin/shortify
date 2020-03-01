from . import redis_client


class RedisClient:
	""" Wrapper class for Redis client"""

	def __init__(self):
		self._client = redis_client


	def set_short_url(self, long_url, user_id, short_url):
		key = f"{long_url}:{user_id}"
		self._client.set(key, short_url)


	def set_long_url(self, short_url, long_url):
		self._client.set(short_url, long_url)


	def get_short_url(self, long_url, user_id):
		key = f"{long_url}:{user_id}"

		return self._client.get(key)


	def get_long_url(self, short_url):

		return self._client.get(short_url)


	def delete_short_url(self, long_url, user_id):
		key = f"{long_url}:{user_id}"
		redis_client.delete(key)


	def delete_long_url(self, short_url):
		redis_client.delete(short_url)
