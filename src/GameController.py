from src.Game import Game
from src.Players import *
import random
from Bot import bot

class GameController:
    def __init__(self):
        self.game = Game()
        self.is_Started = False
        self.owner_id = None
        self.players_ids = []

    def set_started_status(self):
        self.is_Started = True

    def set_owner_id(self, owner_id):
        self.owner_id = owner_id

    def add_player_id(self, player_id):
        self.players_ids.append(player_id)

    def set_roles(self):
        p_ids = self.players_ids.copy()

        werewolves_number = 3 if len(p_ids) >= 16 else 2

        sage_id = random.choice(p_ids)
        sage = Sage(sage_id)
        self.game.add_player(sage)
        self.game.sage = sage
        p_ids.remove(sage_id)

        medic_id = random.choice(p_ids)
        medic = Medic(medic_id)
        self.game.add_player(medic)
        self.game.medic = medic
        p_ids.remove(medic_id)

        for _ in range(werewolves_number):
            werewolf_id = random.choice(p_ids)
            werewolf = Werewolf(werewolf_id)
            self.game.add_player(werewolf)
            self.game.werewolves.append(werewolf)
            p_ids.remove(werewolf_id)

        for player_id in p_ids:
            villager = Villager(player_id)
            self.game.add_player(villager)
            self.game.villagers.append(player_id)

    # sends DM to each player
    async def inform_about_roles(self):
        for player in self.game.players:
            user = await bot.fetch_user(player.id)
            await user.send(f'Your role is {type(player).__name__}')

    async def start_game(self):
        self.game.alive_players = self.game.players.copy()

        await self.inform_about_roles()

        while not self.game.check_game_over():
            self.game.start_night()
            await self.game.sage_checking()
            self.game.start_day()
            # Handle day actions here (example: Villager discussions)
            self.game.tally_votes()

            self.game.update_alive_players()