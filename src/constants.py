from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

BASE_PATH = Path('data')

CFBD_API_KEY = os.getenv('CFBD_API_KEY')
CFBD_URL = 'https://api.collegefootballdata.com'
