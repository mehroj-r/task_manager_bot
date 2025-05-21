import settings
from utils.api_client import ApiClient

class Task:

    def __init__(self, user, title, description = None, due_date = None):
        self.user = user
        self.title = title
        self.description = description
        self.due_date = due_date
        self.api_client = ApiClient(base_url=settings.URL, user=user)

    async def add_task(self):

        payload = {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

        response = await self.api_client.post(endpoint="tasks/", json=payload)

        if response.status_code != 201:
            raise Exception("Can't add task: ", response.text)

        return response.json()

    async def get_tasks(self, cursor=None) -> tuple[dict, str, str]:

        # Define the endpoint
        endpoint = "tasks/"

        if cursor:
            endpoint += f"?cursor={cursor}"

        # Make the GET request
        response = await self.api_client.get(endpoint=endpoint)

        if response.status_code != 200:
            raise Exception("Can't get tasks: ", response.text)

        response_json = response.json()

        return response_json["results"], response_json["next"], response_json["previous"]