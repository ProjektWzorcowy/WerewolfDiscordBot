from token_1 import tokenik
import discord
from discord.ext import commands
from src.Game import Game

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)
game = Game()


def run_bot():
    bot.run(tokenik)


# bot don't react to private messages and messages sent before start of the game
@bot.event
async def on_message(ctx):
    if ctx.guild is not None and (game.is_Started or ctx.content.startswith("!start")):
        await bot.process_commands(ctx)


@bot.command()
async def start(ctx):
    if not game.is_Started:
        await ctx.send("Game preparation started, waiting for players to join...")
        game.owner = ctx.author.id
        game.is_Started = True
        await join(ctx)
    else:
        user = await bot.fetch_user(game.owner)
        await ctx.send(f'Game was already started! Owner of game is: {user.mention}')


@bot.command()
async def join(ctx):
    if game.phase == 'waiting':
        if ctx.author.id not in game.players:
            await ctx.send(f'{ctx.author.mention} has joined!')
            game.players.append(ctx.author.id)
            game.start_night()
        else:
            await ctx.send(f'{ctx.author.mention} You have already joined!')


@bot.command()
async def begin(ctx):
    if game.phase == 'waiting' and ctx.author.id is game.owner:
        player_names = await get_player_names()
        await ctx.send(f'Game has begun! List of players: {player_names}')


# converts list of ids to list of mentions (@username)
async def get_player_names():
    player_names = []
    for player_id in game.players:
        user_mention = await bot.fetch_user(player_id)
        player_names.append(user_mention.mention)
    return player_names

