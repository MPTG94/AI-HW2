"""
MiniMax Player with AlphaBeta pruning and global time
"""
import time
import numpy as np
from copy import deepcopy

from SearchAlgos import AlphaBeta
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
from utils import GameUtils
import utils


class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.utils = GameUtils
        self.game_time = game_time

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
        self.prev_board = None
        self.my_pos = np.full(9, -1)
        self.rival_pos = np.full(9, -1)
        self.turn = 0

        # Extra time management params
        self.initial_balance_factor = (1 / 30)
        self.curr_iteration_runtime = self.game_time * self.initial_balance_factor
        self.safe_runtime_extension = 0.01

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        # TODO: erase the following line and implement this function.
        print(f'======================== Starting turn {self.turn} =========================')
        curr_time_limit = min(self.curr_iteration_runtime, time_limit)
        state = utils.GameState(deepcopy(self.board), self.prev_board, self.my_pos, self.rival_pos, self.turn,
                                time.time() + curr_time_limit - self.safe_runtime_extension)
        search_algo = AlphaBeta(self.utils.utility_method, self.utils.successor_func, None, self.utils.check_goal)
        depth = 1
        best_move = (None, None)

        while True:
            try:
                temp_move = search_algo.search(state, depth, True)
                if temp_move[1] is not None:
                    best_move = temp_move
                else:
                    print(f'GOT NONE!')
                print(f'trying depth {depth}')
            except TimeoutError:
                break
            depth += 1

        # TODO: Update time limits based on some metrics
        move = best_move[1]
        self.prev_board = deepcopy(self.board)
        new_state = utils.GameState(self.board, self.prev_board, self.my_pos, self.rival_pos, self.turn,
                                    time.time() + time_limit)

        GameUtils.perform_move(new_state, move, 1)
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

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm
