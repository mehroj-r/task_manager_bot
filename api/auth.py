import settings
from utils.api_client import ApiClient
from api.utils import hash_data_with_token
from utils.redis_client import RedisClient


class Auth:

    def __init__(self, id, username, first_name, last_name, language_code):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code
        self.api_client = ApiClient(base_url=settings.BASE_URL)
        self.redis_client = RedisClient(redis_url=settings.REDDIS_URL)

    async def get_token(self):

        token = await self.redis_client.get_user_token(self.id)

        if not token:
            return await self.get_new_token()

        return token

    async def get_new_token(self):

        payload = {
            "id": self.id,
            "hash": self.generate_hash(),
        }

        response = await self.api_client.post("token/", json=payload)

        if response.status_code != 200:
            raise Exception("Failed to get token: ", response.text)

        token = response.json()["token"]
        await self.redis_client.save_user_token(self.id, token)

        return token

    async def check_token(self):

        token = await self.redis_client.get_user_token(self.id)

        if not token:
            return False

        payload = {
            "token": await self.redis_client.get_user_token(self.id),
        }

        response = await self.api_client.post("token/verify/", json=payload)

        return response.status_code == 200

    def generate_hash(self):

        data = {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "language_code": self.language_code,
        }

        return hash_data_with_token(data, settings.BOT_API_TOKEN)
