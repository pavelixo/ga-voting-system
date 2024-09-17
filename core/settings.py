from os import getenv
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)
load_dotenv(dotenv_path=BASE_DIR / '.env.example')

BOT_TOKEN = getenv('BOT_TOKEN')
BOT_PREFIX = '>'