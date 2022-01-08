"""
MiniMax Player with AlphaBeta pruning and global time
"""
import statistics
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
        self.initial_game_time = game_time
        self.total_runtime_by_turn = {}

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
        self.initial_balance_factor = (1 / 60)
        self.curr_iteration_runtime = self.game_time * self.initial_balance_factor
        self.safe_runtime_extension = 0.01
        # early: turn >=25
        self.phase2_early_extension = 1.2
        # late: turn >=45
        self.phase2_late_extension = 1.5

        self.phase2_large_blocked_num_factor = (1 / 40)
        self.phase2_large_dead_num_factor = (1 / 40)

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
        state = utils.GameState(deepcopy(self.board), self.prev_board, self.my_pos, self.rival_pos, self.turn,
                                time.time() + curr_time_limit - self.safe_runtime_extension)
        search_algo = AlphaBeta(self.utils.utility_method, self.utils.successor_func, None, self.utils.check_goal)
        depth = 1
        best_move = (None, None)

        while True:
            try:
                if self.turn < 18 and depth == 5:
                    break
                elif self.turn >= 18 and depth == 7:
                    break
                elif depth > self.next_depth_limit:
                    break
                print(f'Starting depth {depth}, with time limit: {curr_time_limit}')
                start_time = time.time()
                temp_move = search_algo.search(state, depth, True)
                end_time = time.time()
                if temp_move[1] is not None:
                    best_move = temp_move
                    try:
                        self.total_runtime_by_turn[self.turn].append(end_time - start_time)
                    except KeyError:
                        self.total_runtime_by_turn[self.turn] = [end_time - start_time]
                    print(self.total_runtime_by_turn)
                else:
                    # TODO: are we sure this is fine?
                    # print(f'GOT NONE!')
                    break
            except TimeoutError:
                break
            depth += 1

        move = best_move[1]
        # ALIVE COUNT
        our_dead_count = 9 - len(GameUtils.get_soldier_position_by_player_index(self.board, 1))
        rival_dead_count = 9 - len(GameUtils.get_soldier_position_by_player_index(self.board, 2))

        # BLOCKED COUNT
        our_blocked_count = GameUtils.count_blocked_soldiers_by_player_index(self.board, 1)
        rival_blocked_count = GameUtils.count_blocked_soldiers_by_player_index(self.board, 2)
        self.prev_board = deepcopy(self.board)
        new_state = utils.GameState(self.board, self.prev_board, self.my_pos, self.rival_pos, self.turn,
                                    time.time() + time_limit)

        GameUtils.perform_move(new_state, move, 1)
        self.turn += 1
        # Need to look at the time the current iteration took
        curr_iteration_runtime = time.time() - move_start_time
        if self.turn > 18:
            # ALIVE COUNT
            new_our_dead_count = 9 - len(GameUtils.get_soldier_position_by_player_index(new_state.board, 1))
            new_rival_dead_count = 9 - len(GameUtils.get_soldier_position_by_player_index(new_state.board, 2))

            # BLOCKED COUNT
            new_our_blocked_count = GameUtils.count_blocked_soldiers_by_player_index(new_state.board, 1)
            new_rival_blocked_count = GameUtils.count_blocked_soldiers_by_player_index(new_state.board, 2)
            if new_rival_blocked_count + new_our_blocked_count >= 6 and \
                    new_our_blocked_count + new_rival_blocked_count > our_blocked_count + rival_blocked_count:
                self.curr_iteration_runtime = curr_iteration_runtime + self.game_time * self.phase2_large_blocked_num_factor
            elif new_rival_blocked_count + new_our_blocked_count < 6 and \
                    new_our_blocked_count + new_rival_blocked_count < our_blocked_count + rival_blocked_count:
                self.curr_iteration_runtime = curr_iteration_runtime - self.game_time * self.phase2_large_blocked_num_factor
            if new_rival_dead_count + new_our_dead_count >= 7 and \
                    new_our_dead_count + new_rival_dead_count > our_dead_count + rival_dead_count:
                self.curr_iteration_runtime = curr_iteration_runtime + self.game_time * self.phase2_large_dead_num_factor
            elif new_rival_dead_count + new_our_dead_count < 7 and \
                    new_our_dead_count + new_rival_dead_count < our_dead_count + rival_dead_count:
                self.curr_iteration_runtime = curr_iteration_runtime - self.game_time * self.phase2_large_dead_num_factor
        else:
            self.curr_iteration_runtime = curr_iteration_runtime
        move_end_time = time.time()
        # Update remaining game time
        self.game_time -= move_end_time - move_start_time
        current_turn_num = self.turn - 1
        if len(self.total_runtime_by_turn[current_turn_num]) > 3 and self.total_runtime_by_turn[current_turn_num][
            3] * 30 < self.game_time < self.total_runtime_by_turn[current_turn_num][
            3] * 70:
            self.next_depth_limit = 4
        if len(self.total_runtime_by_turn[current_turn_num]) > 2 and self.total_runtime_by_turn[current_turn_num][
            2] * 30 < self.game_time < self.total_runtime_by_turn[current_turn_num][
            2] * 70:
            self.next_depth_limit = 3
        if len(self.total_runtime_by_turn[current_turn_num]) > 1 and self.total_runtime_by_turn[current_turn_num][
            1] * 30 < self.game_time < self.total_runtime_by_turn[current_turn_num][
            1] * 70:
            self.next_depth_limit = 2
        else:
            self.next_depth_limit = 1
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
