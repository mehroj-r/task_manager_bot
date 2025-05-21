import requests

import settings
from api.utils import hash_data_with_token
from utils.redis_client import RedisClient


class Auth:

    def __init__(self, user):
        self.user = user
        self.redis_client = RedisClient(redis_url=settings.REDDIS_URL)

    async def get_token(self):

        token = await self.redis_client.get_user_token(self.user.id)

        if not token:
            return await self.get_new_token()

        return token

    async def get_new_token(self):

        payload = {
            "id": self.user.id,
            "hash": self.generate_hash(),
        }

        response = self._post_request(endpoint="token/", data=payload)

        if response.status_code != 200:
            raise Exception("Failed to get token: ", response.text)

        token = response.json()["token"]
        await self.redis_client.save_user_token(self.user.id, token)

        return token

    async def check_token(self):

        token = await self.redis_client.get_user_token(self.user.id)

        if not token:
            return False

        payload = {
            "token": await self.redis_client.get_user_token(self.user.id),
        }

        response = self._post_request(endpoint="token/verify/", data=payload)

        return response.status_code == 200

    def generate_hash(self):

        data = {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "language_code": self.user.language_code,
        }

        return hash_data_with_token(data, settings.BOT_API_TOKEN)

    @staticmethod
    def _post_request(endpoint, data):
        url = f"{settings.BASE_URL}/{endpoint}"
        response = requests.post(url, json=data)
        return response