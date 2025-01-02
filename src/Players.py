from enum import Enum, auto
from src.Bot import get_choice
from src.MessageSender import MessageSender

class PlayerState(Enum):
    ALIVE = auto()
    DEAD = auto()

class ProtectionState(Enum):
    PROTECTED = auto()
    UNPROTECTED = auto()

class Player:
    def __init__(self, id,  state=PlayerState.ALIVE, protection_state = ProtectionState.UNPROTECTED):
        self.id = id
        self.state = state
        self.protection_state = protection_state

    def die(self):
        self.state = PlayerState.DEAD

    async def action(self):
        pass  # To be implemented by subclasses

    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state.name
        }

    @classmethod
    def from_dict(cls, data):
        state = PlayerState[data["state"]]
        return cls(id=data["id"], state=state)


class Villager(Player):
    async def action(self):
        # Villagers typically do not perform special actions at night
        return "Villager is asleep."

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Villager"
        return base_data

    @classmethod
    def from_dict(cls, data):
        player_data = Player.from_dict(data)
        return cls(id=player_data.id, state=player_data.state)

class Werewolf(Player):
    async def action(self, target):
        # Werewolf kills a target
        # Note, some kind of voting will be needed, or one Werewolf is 'Master', only him getting to attack.
        return f"Werewolf {self.id} has attacked {target.id}."

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Werewolf"
        return base_data

    @classmethod
    def from_dict(cls, data):
        player_data = Player.from_dict(data)
        return cls(id=player_data.id, state=player_data.state)

class Sage(Player):
    async def action(self):
        if self.state == PlayerState.ALIVE:
            sage_choice = await get_choice(self.id)
            if isinstance(sage_choice, Werewolf):
                MessageSender.send_to_person(self.id, "Player you've chosen IS a werewolf!")
            else:
                MessageSender.send_to_person(self.id, "Player you've chosen IS NOT a werewolf!")
            

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Sage"
        return base_data

    @classmethod
    def from_dict(cls, data):
        player_data = Player.from_dict(data)
        return cls(id=player_data.id, state=player_data.state)


class Medic(Player):
    async def action(self):
        if self.state == PlayerState.ALIVE:
            medic_choice = await get_choice(self.id)
            medic_choice.protection_state = ProtectionState.PROTECTED
            self.game.controller.messege_sender.send_to_person(self.id, "Player you've chosen will be protected!")

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Medic"
        return base_data

    @classmethod
    def from_dict(cls, data):
        player_data = Player.from_dict(data)
        return cls(id=player_data.id, state=player_data.state)