from token_1 import tokenik
import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)


def run_bot():
    bot.run(tokenik)


# import has to be here to avoid circular import
from src.Game import SpecificGameType
from src.GameController import GameController

game_controller = GameController()
game = SpecificGameType()
game.game_controller = game_controller
game_controller.game = game


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
    if game_controller.game.phase == 'waiting':
        if ctx.author.id not in game_controller.players_ids:
            await ctx.send(f'{ctx.author.mention} has joined!')
            game_controller.add_player_id(ctx.author.id)
        else:
            await ctx.send(f'{ctx.author.mention} You have already joined!')


@bot.command()
async def begin(ctx):
    if game_controller.game.phase == 'waiting' and ctx.author.id is game_controller.owner_id:
        player_mentions = await get_player_mentions()
        await ctx.send(f'Game has begun! List of players: {player_mentions}')
        game_controller.set_roles()
        await game_controller.start_game()


# converts list of ids to list of mentions (@username)
async def get_player_mentions():
    player_names = []
    for player_id in game_controller.players_ids:
        user = await bot.fetch_user(player_id)
        player_names.append(user.mention)
    return player_names


async def interact_with_sage(sage_id):
    pass


async def get_player_names():
    player_names = []
    i = 0
    for player_id in game_controller.players_ids:
        user = await bot.fetch_user(player_id)
        player_names.append(f'{user.name}#{user.discriminator}')
        i += 1
    return player_names


class PlayersDropdown(discord.ui.Select):
    def __init__(self, lst, future):
        options = [
            discord.SelectOption(label=player) for player in lst
        ]
        super().__init__(placeholder="Choose a player", max_values=1, min_values=1, options=options)
        self.lst = lst
        self.future = future

    async def callback(self, interaction: discord.Interaction):
        selected_player = self.values[0]
        selected_player_ind = self.lst.index(selected_player)
        self.future.set_result(selected_player_ind)
        # there is no problem with send_message method availability, although it can show it in PyCharm
        await interaction.response.send_message(f'You chose {selected_player}!')


class PlayersDropdownView(discord.ui.View):
    def __init__(self, lst, future):
        super().__init__()
        self.add_item(PlayersDropdown(lst, future))


async def send_select_player_menu(user_id):
    player_names = await get_player_names()
    future = asyncio.get_event_loop().create_future()

    view = PlayersDropdownView(player_names, future)
    user = await bot.fetch_user(user_id)

    await user.send("Choose a player:", view=view)

    selected_player_ind = await future

    return selected_player_ind


