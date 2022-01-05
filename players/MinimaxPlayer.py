"""
MiniMax Player
"""
import numpy as np

from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
from SearchAlgos import MiniMax
from utils import GameUtils


class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.utils = GameUtils

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        # TODO: erase the following line and implement this function.
        self.board = board
        self.my_pos = np.full(9, -1)
        self.rival_pos = np.full(9, -1)
        self.turn = 0

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        # TODO: erase the following line and implement this function.
        minimax_algo = MiniMax(self.utils.utility_method, self.utils.successor_func, None, self.utils.check_goal)
        if self.turn < 18:
            move = self._stage_1_move()
            self.turn += 1
            return move

        else:
            move = self._stage_2_move()
            self.turn += 1
            return move

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        rival_pos, rival_soldier, my_dead_pos = move

        if self.turn < 18:
            # Currently, still in the first part of the game
            # Update the board to include the new enemy soldier
            self.board[rival_pos] = 2
            # In the array containing the positions of all enemy soldiers, put in the index of the new soldier,
            # it's position on the board
            self.rival_pos[rival_soldier] = rival_pos
        else:
            # Now in the second part of the game
            rival_prev_pos = self.rival_pos[rival_soldier]
            self.board[rival_prev_pos] = 0
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        if my_dead_pos != -1:
            # The enemy player has killed one of our soldiers
            self.board[my_dead_pos] = 0
            # Get from the board the index of the killed soldier
            dead_soldier = int(np.where(self.my_pos == my_dead_pos)[0][0])
            # Mark our killed soldier as dead in our soldiers array
            self.my_pos[dead_soldier] = -2
        self.turn += 1

    def _stage_1_move(self) -> tuple:
        # cell = int(np.where(self.board == 0)[0][0])
        # soldier_that_moved = int(np.where(self.my_pos == -1)[0][0])
        cell, soldier_that_moved = self._stage_1_choose_cell_and_soldier_to_move()
        self.my_pos[soldier_that_moved] = cell
        self.board[cell] = 1

        rival_cell = -1 if not self.is_mill(cell) else self._make_mill_get_rival_cell()
        return cell, soldier_that_moved, rival_cell

    def _stage_1_choose_cell_and_soldier_to_move(self):
        cell = int(np.where(self.board == 0)[0][0])
        # Find a soldier that isn't used already
        soldier_that_moved = int(np.where(self.my_pos == -1)[0][0])
        return cell, soldier_that_moved

    def _stage_2_move(self) -> tuple:
        cell, soldier_that_moved = -1, -1
        soldiers_on_board = np.where(self.board == 1)[0]
        for soldier_cell in soldiers_on_board:
            direction_list = self.directions(int(soldier_cell))
            for direction in direction_list:
                if self.board[direction] == 0:
                    cell = direction
                    soldier_that_moved = int(np.where(self.my_pos == soldier_cell)[0][0])
                    self._update_player_on_board(cell, self.my_pos[soldier_that_moved], soldier_that_moved)
                    rival_cell = -1 if not self.is_mill(cell) else self._make_mill_get_rival_cell()  # Check if mill

                    return cell, soldier_that_moved, rival_cell
        assert cell == -1, 'No moves'

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
