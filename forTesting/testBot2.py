import discord
from discord.ext import commands
from token_2 import t2 as token
from token_2 import target

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)

@bot.event
async def on_ready():
    print("Bot2 is ready.")

@bot.command()
async def join(ctx):
    await ctx.send("!join")

@bot.command()
async def move(ctx):
    user = await bot.fetch_user(target)  # Fetch the user by ID
    await user.send("test")

bot.run(token)
