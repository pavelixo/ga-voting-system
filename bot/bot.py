from nextcord import Intents
from nextcord.ext import commands
from nextcord import Member

from core.settings import BOT_PREFIX
from db.database import Session
from db import crud

intent = Intents.all()
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intent)

@bot.event
async def on_ready():
  print(f"{bot.user.name}")

@bot.command(name='candidatar')
async def apply_for_candidacy(ctx):
  db = Session()
  user_id = ctx.author.id

  try:
    candidate = crud.create_candidate(db=db, user_id=user_id)
    await ctx.send(f"deu bom user_id:{candidate.user_id}")
  except Exception as e:
    await ctx.send(f"{e}")
  finally:
    db.close()

@bot.command(name='desistir')
async def withdraw_candidacy(ctx):
  db = Session()
  user_id = ctx.author.id

  try:
    crud.remove_candidate(db=db,user_id=user_id)
    await ctx.send(f"desistiu {ctx.author.name}")
  finally:
    db.close()

@bot.command(name='votar')
async def add_vote(ctx, user: Member):
  db = Session()
  user_id = user.id

  try:
    candidate = crud.add_vote(db=db, user_id=user_id)
    _user = await bot.fetch_user(user_id)

    await ctx.send(f"o {_user.name} ta com {candidate.votes}")
  finally:
    db.close()