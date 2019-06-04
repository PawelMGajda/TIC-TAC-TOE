from Bot import *
from Player import *


class GameScreenMechanics(Bot, Player):

    def __init__(self, size, win_con):
        super().__init__(size, win_con)

    def move_player(self) -> None:

        self.player_handle_move()

    def move_bot(self) -> None:

        self.bot_handle_move()
        self.player_move_in_progress = True