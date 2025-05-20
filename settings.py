import os
import dotenv

dotenv.load_dotenv()

SERVER = os.environ.get("SERVER")
BOT_API_TOKEN=os.getenv("BOT_API_TOKEN")
REDDIS_URL=os.getenv("REDDIS_URL")

URL=f"{SERVER}/api/v1"
BASE_URL=f"{SERVER}/api"