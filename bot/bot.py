from time import time
from nextcord import Intents
from nextcord.ext import commands
from nextcord import Member
from nextcord.ui import Button, View

from core.settings import BOT_PREFIX
from db.database import Session
from db import crud

intent = Intents.all()
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intent)

@bot.event
async def on_ready():
  print(f"{bot.user.name}")

@bot.command(name='candidatos')
async def get_candidates(ctx):
  start = time()
  db = Session()

  try:
    candidates = crud.get_all_candidates(db=db)
    candidates = [
      {
        "name": (await bot.fetch_user(candidate.user_id)).name, 
        "avatar": (await bot.fetch_user(candidate.user_id)).avatar,
        "votes": candidate.votes
      } 
      for candidate in candidates
    ]
    final = str()
    for candidate in candidates:
      final += f"negueba {candidate['name']} tem {candidate['votes']}\n"
    await ctx.send(final)

  finally:
    db.close()
    end = time()
    await ctx.send(f'rodou em {start-end}')
  
@bot.command(name='candidatar')
async def apply_for_candidacy(ctx):
  db = Session()
  user_id = ctx.author.id
  username = ctx.author.name
  avatar_url = ctx.author.display_avatar.url
  
  try:
    candidate = crud.create_candidate(
      db=db, user_id=user_id, username=username, avatar_url=avatar_url
    )
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