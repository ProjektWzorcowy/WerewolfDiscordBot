from enum import Enum, auto

class PlayerState(Enum):
    ALIVE = auto()
    DEAD = auto()

class Player:
    def __init__(self, id, state=PlayerState.ALIVE):
        self.id = id
        self.state = state

    def die(self):
        self.state = PlayerState.DEAD

    def action(self):
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
    def action(self):
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
    def action(self, target):
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
    def action(self, target):
        # Sage can identify whether a player is a Werewolf
        if isinstance(target, Werewolf):
            return f"Sage {self.id} sees that {target.id} is a Werewolf."
        else:
            return f"Sage {self.id} sees that {target.id} is not a Werewolf."

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Sage"
        return base_data

    @classmethod
    def from_dict(cls, data):
        player_data = Player.from_dict(data)
        return cls(id=player_data.id, state=player_data.state)


class Medic(Player):
    def action(self, targert):
        return "..."

    def to_dict(self):
        base_data = super().to_dict()
        base_data["role"] = "Medic"
        return base_data

    @classmethod
    def from_dict(cls, data):
        player_data = Player.from_dict(data)
        return cls(id=player_data.id, state=player_data.state)