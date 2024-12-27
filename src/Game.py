from src.Players import *
from Bot import bot

class Game:
    def __init__(self):
        self.game_controller = None
        self.players = []
        self.phase = "waiting"  # waiting, night, day
        self.votes = {}


    def add_player(self, player):
        self.players.append(player)

    def start_night(self):
        self.phase = "night"
        print("Night begins. Players take their actions.")

    def start_day(self):
        self.phase = "day"
        print("Day begins. Players discuss and vote.")
        
    def vote(self, voter, target):
        if voter.state == PlayerState.ALIVE and target.state == PlayerState.ALIVE:
            self.votes[voter.id] = target.id

    def tally_votes(self):
        tally = {}
        for vote in self.votes.values():
            tally[vote] = tally.get(vote, 0) + 1
        
        # Find the player with the most votes
        most_voted = max(tally, key=tally.get)
        for player in self.players:
            if player.id == most_voted:
                player.die()
                print(f"{player.id} was executed by the village.")

        self.votes.clear()

    def check_game_over(self):
        pass


class SpecificGameType(Game):
    def check_game_over(self):
        werewolves = [p for p in self.players if isinstance(p, Werewolf) and p.state == PlayerState.ALIVE]
        villagers = [p for p in self.players if not isinstance(p, Werewolf) and p.state == PlayerState.ALIVE]
        
        if not werewolves:
            print("Villagers win!")
            return True
        if len(werewolves) >= len(villagers):
            print("Werewolves win!")
            return True
            
        return False
