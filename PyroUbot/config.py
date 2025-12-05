import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

DEVS = list(map(int, os.getenv("DEVS", "7985641590").split()))

API_ID = int(os.getenv("API_ID", "26235276"))

API_HASH = os.getenv("API_HASH", "c1600609269efc8f691eac7ef200c5cc")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8554159648:AAHH9yRbsno6pepzCe8dY74bGW_cIrlgT4E")

OWNER_ID = int(os.getenv("OWNER_ID", "7985641590"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002523383102").split()))

RMBG_API = os.getenv("RMBG_API", "5db565c7dd8f0a7646cc5c9757dba601")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://viosajagant:viosajagant12A@cluster0.jzkeo4t.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true") 
LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1003257909396"))
