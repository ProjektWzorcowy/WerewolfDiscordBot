from abc import ABC, abstractmethod
from src.Players import Villager, Werewolf, Sage, Medic, Fox

class PlayerFactory(ABC):
    @abstractmethod
    def create_player(self, id):
        pass

class VillagerFactory(PlayerFactory):
    def create_player(self, id):
        return Villager(id)
        
class WerewolfFactory(PlayerFactory):
    def create_player(self, id):
        return Werewolf(id)
        
class SageFactory(PlayerFactory):
    def create_player(self, id):
        return Sage(id)
        
class MedicFactory(PlayerFactory):
    def create_player(self, id):
        return Medic(id)
        
class FoxFactory(PlayerFactory):
    def create_player(self, id):
        return Fox(id)

