from token_1 import tokenik
import discord
from discord.ext import commands
from src.Game import Game
from src.GameController import GameController

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)
game_controller = GameController()
game = Game()
game_controller.game = game


def run_bot():
    bot.run(tokenik)


# bot don't react to private messages and messages sent before start of the game
@bot.event
async def on_message(ctx):
    if ctx.guild is not None and (game_controller.is_Started or ctx.content.startswith("!start")):
        await bot.process_commands(ctx)


@bot.command()
async def start(ctx):
    if not game_controller.is_Started:
        await ctx.send("Game preparation started, waiting for players to join...")
        game_controller.set_owner_id(ctx.author.id)
        game_controller.set_started_status()
        await join(ctx)
    else:
        user = await bot.fetch_user(game_controller.owner_id)
        await ctx.send(f'Game was already started! Owner of game is: {user.mention}')


@bot.command()
async def join(ctx):
    if game.phase == 'waiting':
        if ctx.author.id not in game_controller.players_ids:
            await ctx.send(f'{ctx.author.mention} has joined!')
            game_controller.add_player_id(ctx.author.id)
        else:
            await ctx.send(f'{ctx.author.mention} You have already joined!')


@bot.command()
async def begin(ctx):
    if game.phase == 'waiting' and ctx.author.id is game_controller.owner_id:
        player_names = await get_player_names()
        await ctx.send(f'Game has begun! List of players: {player_names}')
        game_controller.set_roles()
        game_controller.start_game()


# converts list of ids to list of mentions (@username)
async def get_player_names():
    player_names = []
    for player_id in game_controller.players_ids:
        user_mention = await bot.fetch_user(player_id)
        player_names.append(user_mention.mention)
    return player_names
