from bot.bot import bot
from db.create_tables import create_tables_if_not_exists
from core.settings import BOT_TOKEN

if __name__ == '__main__':
  create_tables_if_not_exists()
  bot.run(BOT_TOKEN)