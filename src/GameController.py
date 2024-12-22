from src import Game
from src import Players

class GameController:
    def __init__(self):
        self.game = Game()

    def invite(self, id, role):
        # Note: We probably should make it so player is assigned a role automatically, randomly.
        if role == "Villager":
            player = Players.Villager(id)
        elif role == "Werewolf":
            player = Players.Werewolf(id)
        elif role == "Sage":
            player = Players.Sage(id)
        else:
            raise ValueError("Unknown role")

        self.game.add_player(player)
        print(f"Player {id} with role {role} has been added.")

    def start_game(self):
        print("Game started. Let the hunt begin!")
        while not self.game.check_game_over():
            self.game.start_night()
            # Handle night actions here (example: Werewolf kills)
            self.game.start_day()
            # Handle day actions here (example: Villager discussions)
            self.game.tally_votes()