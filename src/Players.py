from enum import Enum, auto

class PlayerState(Enum):
    ALIVE = auto()
    DEAD = auto()

class Player:
    def __init__(self, id):
        self.id = id
        self.state = PlayerState.ALIVE

    def die(self):
        self.state = PlayerState.DEAD

    def action(self):
        pass  # To be implemented by subclasses


class Villager(Player):
    def action(self):
        # Villagers typically do not perform special actions at night
        return "Villager is asleep."

class Werewolf(Player):
    def action(self, target):
        # Werewolf kills a target
        # Note, some kind of voting will be needed, or one Werewolf is 'Master', only him getting to attack.
        return f"Werewolf {self.id} has attacked {target.id}."

class Sage(Player):
    def action(self, target):
        # Sage can identify whether a player is a Werewolf
        if isinstance(target, Werewolf):
            return f"Sage {self.id} sees that {target.id} is a Werewolf."
        else:
            return f"Sage {self.id} sees that {target.id} is not a Werewolf."

class Medic(Player):
    def action(self, targert):
        return "..."