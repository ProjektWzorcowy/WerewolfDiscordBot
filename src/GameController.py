from src.Game import Game
from src.MessageSender import MessageSender
from src.Players import *
import random


class GameController:
    def __init__(self):
        self.game = Game(self)
        self.is_Started = False
        self.owner_id = None
        self.players_ids = []
        self.messege_sender = None
    
    def set_message_sender(self, bot, gamechannelid):
        self.messege_sender = MessageSender(bot, gamechannelid)

    def set_started_status(self):
        self.is_Started = True

    def set_owner_id(self, owner_id):
        self.owner_id = owner_id

    def add_player_id(self, player_id):
        self.players_ids.append(player_id)

    async def set_roles(self):
        p_ids = self.players_ids.copy()

        if len(p_ids) < 3:
            MessageSender.send_to_gamechannel("The number of players is too low! Cannot start a game")
            raise ValueError("The number of players is too low to start the game.")

        role_number = 1  # Starting role number

        # Assign roles dynamically using the factory
        while p_ids:
            # Get the next role factory for the current role_number
            factory_class = await self.game.get_next_role_factory(role_number)
            
            player_id = random.choice(p_ids)
            factory = factory_class()
            player = factory.create_player(player_id, self.game)
            
            self.game.add_player(player)
            
            p_ids.remove(player_id)
            role_number += 1



    # sends DM to each player
    async def inform_about_roles(self):
        for player in self.game.players:
            await self.messege_sender.send_to_person(player.id, player.role)
            

    async def start_game(self):
        self.game.alive_players = self.game.players.copy()
        self.game.split_into_teams()
        await self.inform_about_roles()

        while not self.game.check_game_over():
            await self.game.start_night()
            # TODO: Make it so the game waits for a set time, rather than waiting for all actions to be taken
            await self.game.start_day()
            # TODO: Same
            self.game.update_alive_players()

        self.messege_sender.send_to_gamechannel("Game ends! The winning team is: " + self.game.winning_team + "!")
