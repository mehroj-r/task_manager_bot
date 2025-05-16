import settings
from api.auth import Auth
from utils.api_client import ApiClient

class Task:

    def __init__(self, user, title, description = None, due_date = None):
        self.user = user
        self.title = title
        self.description = description
        self.due_date = due_date
        self.api_client = ApiClient(base_url=settings.URL)

    async def add_task(self):

        payload = {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

        # Authorize ApiClient
        await self.authorize(self.user)

        response = await self.api_client.post(endpoint="tasks/", json=payload)

        if response.status_code != 201:
            raise Exception("Can't add task: ", response.text)

        return response.json()

    async def get_tasks(self):

        # Authorize ApiClient
        await self.authorize(self.user)

        response = await self.api_client.get(endpoint="tasks/")

        if response.status_code != 200:
            raise Exception("Can't get tasks: ", response.text)

        return response.json()

    async def authorize(self, user):
        token = await Auth(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
        ).get_token()

        self.api_client.default_headers['Authorization'] = f'Bearer {token}'


