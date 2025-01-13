from abc import ABC, abstractmethod
from src.Players import Villager, Werewolf, Sage, Medic, Fox

class PlayerFactory(ABC):
    @abstractmethod
    def create_player(self, id, game):
        pass

class VillagerFactory(PlayerFactory):
    def create_player(self, id, game):
        return Villager(id, game)
        
class WerewolfFactory(PlayerFactory):
    def create_player(self, id, game):
        return Werewolf(id, game)
        
class SageFactory(PlayerFactory):
    def create_player(self, id, game):
        return Sage(id, game)
        
class MedicFactory(PlayerFactory):
    def create_player(self, id, game):
        return Medic(id, game)
        
class FoxFactory(PlayerFactory):
    def create_player(self, id, game):
        return Fox(id, game)

