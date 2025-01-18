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
        self.role = "deafult"
        self.protection_state = protection_state

    def die(self):
        self.state = PlayerState.DEAD

    def test(self):
        print(self.role)
        print(self.state)
        print(self.protection_state)
        print("-------------")
        return True

    async def action(self):
        pass  # To be implemented by subclasses

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "state": self.state.name
        }

    @classmethod
    def from_dict(cls, data):
        state = PlayerState[data["state"]]
        match data["role"]:
            case "Villager":
                return Villager.from_dict(data)
            case "Werewolf":
                return Werewolf.from_dict(data)
            case "Sage":
                return Sage.from_dict(data)
            case "Medic":
                return Medic.from_dict(data)
            case "Fox":
                return Fox.from_dict(data)

        return cls(id=data["id"], state=state)


class Villager(Player):
    role = "Villager"
    
    def __init__(self, id, state = PlayerState.ALIVE):
        super().__init__(id, state)
        self.role = self.__class__.role  # Explicitly set the role

    async def action(self):
        # Villagers typically do not perform special actions at night
        return "Villager is asleep."

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Villager"
        return base_data

    @classmethod
    def from_dict(cls, data):
        state = PlayerState[data["state"]]
        return cls(id=data["id"], state=state)

class Werewolf(Player):
    role = "Werewolf"
    
    def __init__(self, id, state = PlayerState.ALIVE):
        super().__init__(id, state)
        self.role = self.__class__.role  # Explicitly set the role

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
        state = PlayerState[data["state"]]
        return cls(id=data["id"], state=state)

class Sage(Player):
    role = "Sage"
    
    def __init__(self, id, state = PlayerState.ALIVE):
        super().__init__(id, state)
        self.role = self.__class__.role  # Explicitly set the role

    async def action(self):
        if self.state == PlayerState.ALIVE:
            sage_choice = await get_choice(self.id)
            print(sage_choice.role)
            if isinstance(sage_choice, Werewolf):
                return("Player you've chosen IS a werewolf!")
            else:
                return("Player you've chosen IS NOT a werewolf!")
            

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Sage"
        return base_data

    @classmethod
    def from_dict(cls, data):
        state = PlayerState[data["state"]]
        return cls(id=data["id"], state=state)


class Medic(Player):
    role = "Medic"
    
    def __init__(self, id, state = PlayerState.ALIVE):
        super().__init__(id, state)
        self.role = self.__class__.role  # Explicitly set the role

    async def action(self):
        if self.state == PlayerState.ALIVE:
            medic_choice = await get_choice(self.id)
            medic_choice.protection_state = ProtectionState.PROTECTED
            return("Player you've chosen will be protected!")

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Medic"
        return base_data

    @classmethod
    def from_dict(cls, data):
        state = PlayerState[data["state"]]
        return cls(id=data["id"], state=state)
    

class Fox(Player):
    role = "fox"
    
    def __init__(self, id, state = PlayerState.ALIVE):
        super().__init__(id, state)
        self.role = self.__class__.role  # Explicitly set the role

    async def action(self):
        if self.state == PlayerState.ALIVE:
            self.ProtectionState = ProtectionState.PROTECTED
            return("Fox hides away from the werewolfs")

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Fox"
        return base_data

    @classmethod
    def from_dict(cls, data):
        state = PlayerState[data["state"]]
        return cls(id=data["id"], state=state)
    
