import os
import dotenv

dotenv.load_dotenv()

URL="http://167.172.55.141:8005/api/v1"
BASE_URL="http://167.172.55.141:8005/api"
BOT_API_TOKEN=os.getenv("BOT_API_TOKEN")
REDDIS_URL=os.getenv("REDDIS_URL")