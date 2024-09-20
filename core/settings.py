from os import getenv
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)
load_dotenv(dotenv_path=BASE_DIR / '.env.example')

BOT_TOKEN = getenv('BOT_TOKEN')
BOT_PREFIX = '>'

GUILD_ID = 1217879394941534330
ELECTIONS_CHANNEL = 1286044634853675059
