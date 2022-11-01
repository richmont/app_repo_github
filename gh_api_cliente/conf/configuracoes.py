import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GH_API_BASE_URL = os.environ.get("GH_API_BASE_URL")
GH_USUARIOS_ENDPOINT = os.environ.get("GH_USUARIOS_ENDPOINT")
PERSONAL_TOKEN = os.environ.get("PERSONAL_TOKEN")