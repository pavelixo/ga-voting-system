from time import time
from random import choices

import nextcord
from nextcord import Intents
from nextcord.ext import commands
from nextcord import Member
from nextcord.ext import tasks

from core.settings import BOT_PREFIX, GUILD_ID, ELECTIONS_CHANNEL
from db.database import Session
from db import crud

intent = Intents.all()
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intent)

@tasks.loop(seconds=15)
async def update_stats(channel):
  stats_message = await channel.fetch_message(1286700665678336091)
  try:
    db = Session()

    top_candidate = crud.get_top_candidate(db=db)
    candidate_count = crud.get_candidate_count(db=db)
    top_5_candidates = crud.get_top_candidates(db=db)

    user = await bot.fetch_user(top_candidate.user_id) 
    embed = nextcord.Embed(title="Eleições Gameplay Avançada", color=nextcord.Color.blue())
    embed.add_field(name=f"1º {top_candidate.username} com {top_candidate.votes} votos", value="\u200b", inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)

    for index, candidate in enumerate(top_5_candidates[1:], start=2):
      embed.add_field(name=f"{index}º {candidate.username} com {candidate.votes} votos", value="\u200b", inline=False)
    
    embed.add_field(name=f"Total de Candidatos: {candidate_count}", value="\u200b", inline=True)
    await stats_message.edit(embed=embed)
  finally:
    db.close()

@bot.event
async def on_ready():
  print(f"{bot.user.name}")
  update_stats.start(bot.get_channel(ELECTIONS_CHANNEL))

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