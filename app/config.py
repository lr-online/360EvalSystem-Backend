import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG").lower() == "true"

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB = os.getenv("MONGODB_DB")
