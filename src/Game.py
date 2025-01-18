from src.Players import *
from src.PlayerFactory import *
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
        self.controller = controller
        self.winning_team = "NONE"

    def add_player(self, player):
        self.players.append(player)
    
    def split_into_teams():
        pass

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
                user = await bot.fetch_user(player.id)
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
            await self.controller.messege_sender.send_to_person(player.id, "Choose a person to LYNCH")
            targeted_player = await get_choice(player.id)
            self.vote(player, targeted_player)
        # Rather than voting one by one, we handle them all at the same time:
        voting_tasks = [handle_vote(player) for player in self.alive_players]
        await asyncio.gather(*voting_tasks)

        await self.tally_votes()

    async def get_next_role(self, role_number):
        pass

class LurkingWerewolf(Game):
    def check_game_over(self):
        werewolves = [p for p in self.players if isinstance(p, Werewolf) and p.state == PlayerState.ALIVE]
        villagers = [p for p in self.players if not isinstance(p, Werewolf)  and p.state == PlayerState.ALIVE]

        if not werewolves:
            print("Villagers win!")
            self.winning_team = "Villagers"
            return True
        if len(werewolves) >= len(villagers):
            print("Werewolves win!")
            self.winning_team = "Werewolves"
            return True
        
        return False
    
    def split_into_teams(self):
        self.werewolves = [p for p in self.players if isinstance(p, Werewolf)]
        self.villagers = [p for p in self.players if not isinstance(p, Werewolf)]
    
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
            await self.werewolf_vote(player, targeted_player)
        # Rather than voting one by one, we handle them all at the same time:
        voting_tasks = [asyncio.create_task(handle_vote(werewolf)) for werewolf in self.werewolves if werewolf.state == PlayerState.ALIVE]
        await asyncio.gather(*voting_tasks)

        return await self.tally_werewolf_votes()


    async def start_night(self):
        self.phase = "night"
        print("Night begins. Players take their actions.")
        villagers_action_tasks = [asyncio.create_task(self.controller.messege_sender.send_to_person(v.id, await v.action())) for v in self.villagers]
        werewolf_victim = await self.werewolf_voting()
        print(werewolf_victim.id)
        # We wait for all villager tasks.
        await asyncio.gather(*villagers_action_tasks)
        #We kill the attacke player, as long as they were not protected
        if(werewolf_victim.protection_state == ProtectionState.UNPROTECTED):
            werewolf_victim.die()
            await self.controller.messege_sender.send_to_person(werewolf_victim.id, "You were KILLED by werewolves!")
        #Reset the protection state
        for player in self.players:
            player.protection_state = ProtectionState.UNPROTECTED

    async def get_next_role_factory(self, role_number):
        if(role_number == 2 or role_number == 8 or role_number == 13):
            return WerewolfFactory
        if(role_number == 3):
            return SageFactory
        if(role_number == 4):
            return MedicFactory
        return VillagerFactory

class CrazyFox(Game):
    def check_game_over(self):
        werewolves = [p for p in self.players if isinstance(p, Werewolf) and p.state == PlayerState.ALIVE]
        villagers = [p for p in self.players if not isinstance(p, Werewolf) and  not isinstance(p, Fox)  and p.state == PlayerState.ALIVE]
        foxes = [p for p in self.players if isinstance(p, Fox) and p.state == PlayerState.ALIVE]
        if not werewolves:
            if not foxes:
                print("Villagers win!")
                self.winning_team = "Villagers"
                return True
            else:
                print("Foxes win!")
                self.winning_team = "Foxes"
                return True
            
        if len(werewolves) >= len(villagers):
            if not foxes:
                print("Werewolves win!")
                self.winning_team = "Werewolves"
                return True
            else:
                print("Foxes win!")
                self.winning_team = "Foxes"
                return True
        
        return False
    
    def split_into_teams(self):
        self.werewolves = [p for p in self.players if isinstance(p, Werewolf)]
        self.villagers = [p for p in self.players if not isinstance(p, Werewolf) and not isinstance(p, Fox)]
        self.foxes = [p for p in self.players if isinstance(p, Fox)]
    
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
        foxes_action_tasks = [asyncio.create_task(v.action()) for v in self.foxes]
        werewolf_victim = await self.werewolf_voting()
        # We wait for all villager and foxes tasks.
        await asyncio.gather(*villagers_action_tasks)
        await asyncio.gather(*foxes_action_tasks)
        #We kill the attacke player, as long as they were not protected
        if(werewolf_victim.ProtectionState == ProtectionState.UNPROTECTED):
            werewolf_victim.die()
        #Reset the protection state
        for player in self.players:
            player.ProtectionState = ProtectionState.UNPROTECTED

    async def get_next_role_factory(self, role_number):
        if(role_number == 2):
            return FoxFactory
        if(role_number == 3 or role_number == 8 or role_number == 13):
            return WerewolfFactory
        if(role_number == 4):
            return SageFactory
        if(role_number == 5):
            return MedicFactory
        return VillagerFactory


class Politics(Game):
    def check_game_over(self):
        werewolves = [p for p in self.players if isinstance(p, Werewolf) and p.state == PlayerState.ALIVE]
        villagers = [p for p in self.players if not isinstance(p, Werewolf)  and p.state == PlayerState.ALIVE]

        if not werewolves:
            print("Villagers win!")
            self.winning_team = "Villagers"
            return True
        if len(werewolves) >= len(villagers):
            print("Werewolves win!")
            self.winning_team = "Werewolves"
            return True
        
        return False
    
    def split_into_teams(self):
        self.werewolves = [p for p in self.players if isinstance(p, Werewolf)]
        self.villagers = [p for p in self.players if not isinstance(p, Werewolf)]

    async def get_next_role_factory(self, role_number):
        if(role_number == 2 or role_number == 7  or role_number  == 11):
            return WerewolfFactory
        return VillagerFactory


    async def start_night(self):
        self.phase = "night"
        print("Night begins. Players do not take their actions.")