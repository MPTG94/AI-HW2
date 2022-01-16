"""
MiniMax Player with AlphaBeta pruning and global time
"""
import statistics
import time
import numpy as np
from copy import deepcopy

from SearchAlgos import AlphaBeta, GameState, GameUtils
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
import utils


class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.utils = GameUtils
        self.game_time = game_time
        self.initial_game_time = game_time
        self.total_runtime_by_turn = {}
        self.runtime_limits = []

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
        self.next_depth_limit = np.inf

        # Extra time management params
        self.safety_time = min(self.initial_game_time * 0.05, 5)
        self.early_runtime = (self.initial_game_time - self.safety_time) * 8 / 10
        self.curr_iteration_runtime = self.early_runtime * 1 / 30
        self.late_runtime = (self.initial_game_time - self.safety_time) * (2 / 10) * (1 / 20)

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
        move_start_time = time.time()
        curr_time_limit = self.curr_iteration_runtime
        self.runtime_limits.append(curr_time_limit)
        state = GameState(deepcopy(self.board), self.prev_board, self.my_pos, self.rival_pos, self.turn,
                          time.time() + curr_time_limit - self.safe_runtime_extension, False)
        search_algo = AlphaBeta(self.utils.utility_method, self.utils.successor_func, None, self.utils.check_goal)
        depth = 1
        best_move = (None, None)

        print('curr time limit:', curr_time_limit)
        while True:
            try:
                if self.turn < 18 and depth == 5:
                    break
                elif self.turn >= 18 and depth == 7:
                    break
                elif depth > self.next_depth_limit:
                    break
                # print(f'Starting depth {depth}, with time limit: {curr_time_limit}')
                start_time = time.time()
                temp_move = search_algo.search(state, depth, True)
                end_time = time.time()
                print(f'{depth}: {end_time - start_time}')
                if temp_move[1] is not None:
                    # print(f'found move')
                    best_move = temp_move
                else:
                    # print(f'GOT NONE!')
                    break
            except TimeoutError:
                break
            depth += 1

        move = best_move[1]
        self.prev_board = deepcopy(self.board)
        new_state = GameState(self.board, self.prev_board, self.my_pos, self.rival_pos, self.turn,
                              time.time() + time_limit, False)

        GameUtils.perform_move(new_state, move, 1)
        self.turn += 1
        move_end_time = time.time()
        self.game_time -= move_end_time - move_start_time
        if self.turn == 10 or self.turn == 11:
            # if 10 <= self.turn <= 20:
            self.curr_iteration_runtime *= 1.5
        if self.turn == 20 or self.turn == 21:
            self.curr_iteration_runtime *= 2.5
        if self.turn == 25 or self.turn == 26:
            self.curr_iteration_runtime /= 2.5
            self.curr_iteration_runtime *= 1.2
        if self.turn > 30:
            print('Now runtime will be:', self.late_runtime)
            self.curr_iteration_runtime = self.late_runtime
        if self.turn > 70:
            self.curr_iteration_runtime = 0.2
        # if self.turn > 19:
        #     self.curr_iteration_runtime = max(0.04, self.curr_iteration_runtime)
        # if self.game_time < 0.5:
        #     self.curr_iteration_runtime = 0.08
        print(f'Time remaining: {self.game_time}')
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

    def calculate_actual_turn_runtime(self):
        sum = 0
        for value in self.total_runtime_by_turn[self.turn]:
            sum += value

        return sum

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm
