import os
import json
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

db_name = os.getenv("DB_NAME")
mongo_uri = os.getenv("MONGODB_URI")
api_id= os.getenv("API_ID")
api_hash= os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
Channel_chat_id = int(os.getenv("CHANNEL_ID"))
admins = json.loads(os.getenv("ADMINS") if os.getenv("ADMINS") else "[]")