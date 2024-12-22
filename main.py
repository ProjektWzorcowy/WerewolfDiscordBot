from token_1 import tokenik
# Wazne rzeczy:
import discord
from discord.ext import commands
import asyncio
import json
import random
import threading
import requests

# Potrzebne zawsze, ustawiasz prefix.
client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)
#event
@client.event
async def on_ready():
    print("Online!")
    print("------------------")
#losowa komenda:
@client.command()
async def hello(ctx):
    await ctx.send("no hej!")

client.run(tokenik)