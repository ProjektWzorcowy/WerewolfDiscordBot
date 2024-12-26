from src.Game import Game
from src.Players import *
import random


class GameController:
    def __init__(self):
        self.is_Started = False
        self.owner_id = None
        self.players_ids = []
        self.game = Game()

    def set_started_status(self):
        self.is_Started = True

    def set_owner_id(self, owner_id):
        self.owner_id = owner_id

    def add_player_id(self, player_id):
        self.players_ids.append(player_id)

    def set_roles(self):
        werewolves_number = 3 if len(self.players_ids) >= 16 else 2

        sage_id = random.choice(self.players_ids)
        self.game.add_player(Sage(sage_id))
        self.players_ids.remove(sage_id)

        medic_id = random.choice(self.players_ids)
        self.game.add_player(Medic(medic_id))
        self.players_ids.remove(medic_id)

        for _ in range(werewolves_number):
            werewolf_id = random.choice(self.players_ids)
            self.game.add_player(Werewolf(werewolf_id))
            self.players_ids.remove(werewolf_id)

        for player_id in self.players_ids:
            self.game.add_player(Villager(player_id))

    def start_game(self):
        print("Game started. Let the hunt begin!")
        while not self.game.check_game_over():
            self.game.start_night()
            # Handle night actions here (example: Werewolf kills)
            self.game.start_day()
            # Handle day actions here (example: Villager discussions)
            self.game.tally_votes()