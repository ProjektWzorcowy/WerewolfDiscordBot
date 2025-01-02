from src.Players import *
from src.MessageSender import MessageSender
from src.Bot import bot
import asyncio


class Game:
    def __init__(self, controller):
        self.players = []
        self.alive_players = []
        self.phase = "waiting"  # waiting, night, day
        self.votes = {}
        self.werewolves_votes = {}
        self.sage = None
        self.medic = None
        self.werewolves = []
        self.villagers = []
        self.medic_target = None
        self.game_channel = None
        self.controller = controller

    def add_player(self, player):
        self.players.append(player)

    def update_alive_players(self):
        for player in self.players:
            if player.state == PlayerState.DEAD:
                self.alive_players.remove(player)

    async def start_night(self):
        pass
        #night depends on implementation

    async def start_day(self):
        self.phase = "day"
        print("Day begins. Players discuss and vote.")
        await self.voting()
        
    def vote(self, voter, target):
        if voter.state == PlayerState.ALIVE and target.state == PlayerState.ALIVE:
            self.votes[voter.id] = target.id

    async def tally_votes(self):
        tally = {}
        for vote in self.votes.values():
            tally[vote] = tally.get(vote, 0) + 1
        
        # Find the player with the most votes
        most_voted = max(tally, key=tally.get)
        for player in self.players:
            if player.id == most_voted:
                player.die()
                user = bot.fetch_user(player.id)
                await self.controller.messege_sender.send_to_gamechannel(f'{user.name} got executed!')

        self.votes.clear()

    def check_game_over(self):
        pass

    async def werewolf_killing(self):
        for werewolf in self.werewolves:
            if werewolf.state == PlayerState.ALIVE:
                targeted_player = await get_choice(werewolf.id)
                self.vote(werewolf, targeted_player)
        await self.tally_votes()

async def voting(self):
    async def handle_vote(player):
        targeted_player = await get_choice(player.id)
        self.vote(player, targeted_player)
    # Rather than voting one by one, we handle them all at the same time:
    voting_tasks = [handle_vote(player) for player in self.alive_players]
    await asyncio.gather(*voting_tasks)

    await self.tally_votes()

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
    
    async def tally_werewolf_votes(self):
        tally = {}
        for vote in self.werewolves_votes.values():
            tally[vote] = tally.get(vote, 0) + 1
        
        # Find the player with the most votes
        most_voted = max(tally, key=tally.get)
        for player in self.players:
            if player.id == most_voted:
                return player
            
    async def werewolf_vote(self, voter, target):
        if voter.state == PlayerState.ALIVE and target.state == PlayerState.ALIVE:
            self.werewolves_votes[voter.id] = target.id
    
    async def werewolf_voting(self):
        async def handle_vote(player):
            targeted_player = await get_choice(player.id)
            self.werewolf_vote(player, targeted_player)
        # Rather than voting one by one, we handle them all at the same time:
        voting_tasks = [asyncio.create_task(handle_vote(werewolf)) for werewolf in self.werewolves if werewolf.state == PlayerState.ALIVE]
        await asyncio.gather(*voting_tasks)

        return await self.tally_werewolf_votes()


    async def start_night(self):
        self.phase = "night"
        print("Night begins. Players take their actions.")
        villagers_action_tasks = [asyncio.create_task(v.action()) for v in self.villagers]
        werewolf_victim = await self.werewolf_voting()
        # We wait for all villager tasks.
        await asyncio.gather(*villagers_action_tasks)
        #We kill the attacke player, as long as they were not protected
        if(werewolf_victim.ProtectionState == ProtectionState.UNPROTECTED):
            werewolf_victim.die()