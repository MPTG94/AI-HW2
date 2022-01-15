"""Search Algos: MiniMax, AlphaBeta
"""
# TODO: you can import more modules, if needed
# DONE TODO: update ALPHA_VALUE_INIT, BETA_VALUE_INIT in utils
import time
import numpy as np
from copy import deepcopy

from utils import get_directions

ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf  # !!!!!

# These are groups of 5 indexes in which there can be 2 free places and each one of them closes a morris
AVAILABLE_3_PIECES_CONFIGS = [
    # Outer layer:
    [0, 1, 2, 4, 7], [2, 4, 5, 6, 7], [0, 3, 5, 6, 7], [0, 1, 2, 3, 5],
    # Middle layer:
    [8, 9, 10, 12, 15], [10, 12, 13, 14, 15], [8, 11, 13, 14, 15], [8, 9, 10, 11, 13],
    # Inner layer:
    [16, 17, 18, 20, 23], [18, 20, 21, 22, 23], [16, 19, 21, 22, 23], [16, 17, 18, 19, 21],
    # top cross:
    [1, 8, 9, 10, 17],
    # right cross:
    [4, 10, 12, 15, 20],
    # bottom cross:
    [6, 13, 14, 15, 22],
    # left cross:
    [3, 8, 11, 13, 19]]

AVAILABLE_MILL_INDEXES = [[0, 1, 2], [2, 4, 7], [5, 6, 7], [0, 3, 5], [8, 9, 10], [10, 12, 15], [13, 14, 15],
                          [8, 11, 13], [16, 17, 18], [18, 20, 23], [21, 22, 23], [16, 19, 21], [1, 9, 17], [4, 12, 20],
                          [6, 14, 22], [3, 11, 19]]

AVAILABLE_PAIR_INDEXES = [[1, 2], [0, 2], [0, 1], [0, 5], [2, 7], [0, 3], [5, 7], [2, 4], [9, 10], [8, 10], [8, 9],
                          [3, 19], [20, 4], [8, 11], [13, 15], [13, 14], [17, 18], [1, 9], [16, 17], [16, 21], [12, 4],
                          [16, 19], [6, 14], [18, 20], [3, 5], [9, 17], [4, 7], [11, 19], [12, 20], [6, 7], [14, 22],
                          [5, 6], [11, 13], [1, 17], [12, 15], [8, 13], [10, 15], [14, 15], [6, 22], [10, 12], [19, 21],
                          [16, 18], [20, 23], [3, 11], [18, 23], [22, 23], [21, 23], [21, 22]]


class SearchAlgos:
    def __init__(self, utility, succ, perform_move=None, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        # TODO: check if depth starts with a large value which needs to be reduced until 0
        # print('STARTING goal check')
        if self.goal(state) or depth <= 0:
            # print('goal' ,self.goal(state))
            # print('depth', depth)
            return self.utility(state, True), None
        # print('PASSED goal check')
        # print(f'searching for depth {depth}')
        # print(state.max_time)
        i = 1 if maximizing_player else 2
        successor_moves = self.succ(state, i)
        if maximizing_player:
            # This is a MAX node
            curr_max = -np.inf
            curr_move = None
            for move in successor_moves:
                state_copy = deepcopy(state)
                GameUtils.perform_move(state_copy, move, i)
                search_algo = MiniMax(self.utility, self.succ, None, self.goal)
                step_value, step_move = search_algo.search(state_copy, depth - 1, False)
                # if state.turn_number == 1:
                #     print('##############################################')
                #     print('MINIMAX MAXIMIZER H value:', step_value)
                #     print('MINIMAX MAXIMIZER Move:', step_move)
                #     print('##############################################')
                if step_value > curr_max:
                    curr_max = step_value
                    curr_move = move
            return curr_max, curr_move
        else:
            # This is a MIN node
            curr_min = np.inf
            curr_move = None
            for move in successor_moves:
                state_copy = deepcopy(state)
                GameUtils.perform_move(state_copy, move, i)
                search_algo = MiniMax(self.utility, self.succ, None, self.goal)
                step_value, step_move = search_algo.search(state_copy, depth - 1, True)
                # if state.turn_number == 1:
                #     print('##############################################')
                #     print('MINIMAX MINIMIZER H value:', step_value)
                #     print('MINIMAX MINIMIZER Move:', step_move)
                #     print('##############################################')
                if step_value < curr_min:
                    curr_min = step_value
                    curr_move = move
        return curr_min, curr_move


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        if self.goal(state) or depth <= 0:
            # if state.turn_number == 18:
            #     print('GOAL', depth, self.goal(state))
            # print('goal' ,self.goal(state))
            # print('depth', depth)
            # print('GOAL', depth, self.goal(state))
            return self.utility(state, True), None
        # print('PASSED goal check')
        # print(f'searching for depth {depth}')
        # print(state.max_time)
        i = 1 if maximizing_player else 2
        successor_moves = self.succ(state, i)
        # if state.light_player:
        #     print(successor_moves)
        #     if len(successor_moves) == 0:
        #         print('here')
        # print(successor_moves)
        if maximizing_player:
            # This is a MAX node
            curr_max = -np.inf
            curr_move = None
            for move in successor_moves:
                state_copy = deepcopy(state)
                GameUtils.perform_move(state_copy, move, i)
                search_algo = AlphaBeta(self.utility, self.succ, None, self.goal)
                step_value, step_move = search_algo.search(state_copy, depth - 1, False, alpha, beta)
                # if state.turn_number == 1:
                #     print('##############################################')
                #     print('ALPHABETA MAXIMIZER H value:', step_value)
                #     print('ALPHABETA MAXIMIZER Move:', step_move)
                #     print('##############################################')
                if step_value is not None and step_value > curr_max:
                    curr_max = step_value
                    # print('assigning move in max', move)
                    curr_move = move
                alpha = max(alpha, curr_max)
                if beta <= alpha:
                    # Early stopping
                    #     print('TRIM MAX')
                    return None, None
            return curr_max, curr_move
        else:
            # This is a MIN node
            curr_min = np.inf
            curr_move = None
            for move in successor_moves:
                state_copy = deepcopy(state)
                GameUtils.perform_move(state_copy, move, i)
                search_algo = AlphaBeta(self.utility, self.succ, None, self.goal)
                step_value, step_move = search_algo.search(state_copy, depth - 1, True, alpha, beta)
                # if state.turn_number == 1:
                #     print('##############################################')
                #     print('ALPHABETA MINIMIZER H value:', step_value)
                #     print('ALPHABETA MINIMIZER Move:', step_move)
                #     print('##############################################')
                if step_value is not None and step_value < curr_min:
                    curr_min = step_value
                    # print('assigning move in min', move)
                    curr_move = move
                beta = min(beta, curr_min)
                if beta <= alpha:
                    # Early stopping
                    # print('TRIM MIN')
                    return None, None
        return curr_min, curr_move


def is_player(player, pos1, pos2, board):
    """
    Function to check if 2 positions have the player on them
    :param player: 1/2
    :param pos1: position
    :param pos2: position
    :return: boolean value
    """
    if board[pos1] == player and board[pos2] == player:
        return True
    else:
        return False


def check_next_mill(position, player, board):
    """
    Function to check if a player can make a mill in the next move.
    :param position: curren position
    :param board: np.array
    :param player: 1/2
    :return:
    """
    mill = [
        (is_player(player, 1, 2, board) or is_player(player, 3, 5, board)),
        (is_player(player, 0, 2, board) or is_player(player, 9, 17, board)),
        (is_player(player, 0, 1, board) or is_player(player, 4, 7, board)),
        (is_player(player, 0, 5, board) or is_player(player, 11, 19, board)),
        (is_player(player, 2, 7, board) or is_player(player, 12, 20, board)),
        (is_player(player, 0, 3, board) or is_player(player, 6, 7, board)),
        (is_player(player, 5, 7, board) or is_player(player, 14, 22, board)),
        (is_player(player, 2, 4, board) or is_player(player, 5, 6, board)),
        (is_player(player, 9, 10, board) or is_player(player, 11, 13, board)),
        (is_player(player, 8, 10, board) or is_player(player, 1, 17, board)),
        (is_player(player, 8, 9, board) or is_player(player, 12, 15, board)),
        (is_player(player, 3, 19, board) or is_player(player, 8, 13, board)),
        (is_player(player, 20, 4, board) or is_player(player, 10, 15, board)),
        (is_player(player, 8, 11, board) or is_player(player, 14, 15, board)),
        (is_player(player, 13, 15, board) or is_player(player, 6, 22, board)),
        (is_player(player, 13, 14, board) or is_player(player, 10, 12, board)),
        (is_player(player, 17, 18, board) or is_player(player, 19, 21, board)),
        (is_player(player, 1, 9, board) or is_player(player, 16, 18, board)),
        (is_player(player, 16, 17, board) or is_player(player, 20, 23, board)),
        (is_player(player, 16, 21, board) or is_player(player, 3, 11, board)),
        (is_player(player, 12, 4, board) or is_player(player, 18, 23, board)),
        (is_player(player, 16, 19, board) or is_player(player, 22, 23, board)),
        (is_player(player, 6, 14, board) or is_player(player, 21, 23, board)),
        (is_player(player, 18, 20, board) or is_player(player, 21, 22, board))
    ]

    return mill[position]


def is_mill(position, board):
    """
    Return True if a player has a mill on the given position
    :param position: 0-23
    :return:
    """
    if position < 0 or position > 23:
        return False
    p = int(board[position])

    # The player on that position
    if p != 0:
        # If there is some player on that position
        return check_next_mill(position, p, board)
    else:
        return False


class GameUtils():
    @staticmethod
    def get_soldier_position_by_player_index(board, player_index):
        """
        Gets all of the indexes on the board where player_index has a soldier
        :param board: the board
        :param player_index: the player to check
        :return: a list of indexes where val == player_index
        """
        return np.where(board == player_index)[0]

    @staticmethod
    def get_available_moves_by_player_index(board, player_index):
        """
        Counts the number of moves player {player_index} can perform on the board
        :param board: the board
        :param player_index: the player to check
        :return: the number of available moves by all player soldiers
        """
        num_moves = 0
        positions = GameUtils.get_soldier_position_by_player_index(board, player_index)
        for position in positions:
            moves = get_directions(position)
            for move in moves:
                if board[move] == 0:
                    num_moves += 1
        return num_moves

    @staticmethod
    def count_blocked_soldiers_by_player_index(board, player_index):
        num_blocked = 0
        positions = GameUtils.get_soldier_position_by_player_index(board, player_index)
        for position, soldier in enumerate(positions):
            if soldier == player_index:
                moves = get_directions(position)
                can_move = False
                for move in moves:
                    if board[move] == 0:
                        can_move = True
                        break
                if not can_move:
                    num_blocked += 1
        return num_blocked

    @staticmethod
    def can_player_i_move(board, player_index):
        """
        Checks if the player can still move
        :param board: the board
        :param player_index: the player to check
        :return: True if the player can still perform a move, False otherwise
        """
        return GameUtils.get_available_moves_by_player_index(board, player_index) > 0

    @staticmethod
    def count_soldiers_by_player_index(board, player_index):
        return len(GameUtils.get_soldier_position_by_player_index(board, player_index))

    @staticmethod
    def check_winner_by_player_index(state, player_index):
        """
        Checks the win conditions
        :param board: the board
        :param player_index: the player to check if he won
        :return: True if the player won, False otherwise
        """
        if state.turn_number > 18:
            if player_index == 1:
                if not GameUtils.can_player_i_move(state.board, 2) or GameUtils.count_soldiers_by_player_index(
                        state.board, 2) < 3:
                    return True
                return False
            else:
                if not GameUtils.can_player_i_move(state.board, 1) or GameUtils.count_soldiers_by_player_index(
                        state.board, 1) < 3:
                    return True
                return False
        return False

    @staticmethod
    def return_winner(state):
        if GameUtils.check_winner_by_player_index(state, 1):
            return 1
        elif GameUtils.check_winner_by_player_index(state, 2):
            return 2
        return 0

    @staticmethod
    def check_goal(state):
        # We only care if our player won
        # print(f'{state.max_time} ------- {time.time()}')
        if state.max_time is not None and state.max_time <= time.time():
            raise TimeoutError
        return GameUtils.return_winner(state) != 0

    @staticmethod
    def successor_func(state, i):
        """
        For phase 1: return a list of tuples where the tuple is: (where to put soldier, which soldier did we put, which enemy soldier did we kill)
        For phase 2: return a list of tuples where the tuple is: (where to put soldier, which soldier did we put, which enemy soldier did we kill)
        :param state:
        :param i:
        :return:
        """
        if state.turn_number < 18:
            return GameUtils.generate_phase_1_succ_moves_by_player_index(state, i)
        else:
            return GameUtils.generate_phase2_succ_moves_by_player_index(state, i)

    @staticmethod
    def generate_phase_1_succ_moves_by_player_index(state, i):
        # Generate move list for our player
        moves = []
        free_indexes = np.where(state.board == 0)[0]
        rival_index_num = 2 if i == 1 else 1
        for free in free_indexes:
            if i == 1:
                soldier_that_moved = int(np.where(state.player_1_pos == -1)[0][0])
            else:
                soldier_that_moved = int(np.where(state.player_2_pos == -1)[0][0])
            if check_next_mill(free, i, state.board):
                # These are the indexes of enemy soldiers, on the board (for example 19)
                rival_indexes = np.where(state.board == rival_index_num)[0]
                for rival_index in rival_indexes:
                    moves.append((free, soldier_that_moved, rival_index))
            else:
                # Can't kill with this move
                moves.append((free, soldier_that_moved, -1))
        # if state.turn_number == 1:
        #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #     print(moves)
        #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        return moves

    @staticmethod
    def generate_phase2_succ_moves_by_player_index(state, i):
        # Generate move list for our player
        moves = []
        rival_index_num = 2 if i == 1 else 1
        if i == 1:
            player_pos_list = state.player_1_pos
        else:
            player_pos_list = state.player_2_pos
        for soldier_position_on_board in player_pos_list:
            if soldier_position_on_board == -2:
                continue
            current_soldier_index = np.where(player_pos_list == soldier_position_on_board)[0][0]
            directions = get_directions(soldier_position_on_board)
            for direction in directions:
                if state.board[direction] == 0:
                    state.board[soldier_position_on_board] = 0
                    if check_next_mill(direction, i, state.board):
                        rival_indexes = np.where(state.board == rival_index_num)[0]
                        for rival_index in rival_indexes:
                            moves.append((direction, current_soldier_index, rival_index))
                    else:
                        # Can't kill with this move
                        moves.append((direction, current_soldier_index, -1))
                    state.board[soldier_position_on_board] = i
        return moves

    @staticmethod
    def utility_method(state, get_score=False):
        # if get_score:
        #     # Our player won, so we need to return a large value to point minimax in that direction
        #     pass
        h_values = []
        if state.turn_number < 18:
            # print(len(state.stage_1_h_list))
            heuristic_value = 0
            for weight, h_func in zip(state.stage_1_h_weights, state.stage_1_h_list):
                if h_func == Heuristics.was_mill_created:
                    if state.prev_board is not None:
                        heuristic_value += weight * h_func(state)
                    else:
                        continue
                else:
                    heuristic_value += weight * h_func(state)
        else:
            # print(len(state.stage_2_h_list))
            heuristic_value = 0
            for weight, h_func in zip(state.stage_2_h_weights, state.stage_2_h_list):
                if h_func == Heuristics.was_mill_created or h_func == Heuristics.was_mill_broken:
                    if state.prev_board is not None:
                        val = weight * h_func(state)
                        h_values.append(val)
                        heuristic_value += val
                    else:
                        continue
                else:
                    val = weight * h_func(state)
                    h_values.append(val)
                    heuristic_value += val
            # GameUtils.print_heuristic_results(h_values)
        # print(f'PLAYER: {state.my_index}, H_VALUE: {heuristic_value}')
        return heuristic_value

    @staticmethod
    def print_heuristic_results(h_values):
        h_names = ['was_mill_created', 'number_of_closed_mills', 'number_of_blocked_soldiers',
                   'number_of_soldiers_on_board', 'was_mill_broken', 'number_of_double_morris', 'is_goal']
        for name, val in zip(h_names, h_values):
            print(name, val, end=" ")
        print("\n")

    @staticmethod
    def perform_move(state, move, i):
        if i == 1:
            player_pos_list = state.player_1_pos
        else:
            player_pos_list = state.player_2_pos
        if state.turn_number < 18:
            new_soldier_pos, new_soldier_index, rival_enemy_position_on_board = move
            state.board[new_soldier_pos] = i
            if i == 1:
                state.player_1_pos[new_soldier_index] = new_soldier_pos
                if rival_enemy_position_on_board != -1:
                    state.board[rival_enemy_position_on_board] = 0
                    state.player_2_pos[np.where(state.player_2_pos == rival_enemy_position_on_board)[0][0]] = -2
            else:
                state.player_2_pos[new_soldier_index] = new_soldier_pos
                if rival_enemy_position_on_board != -1:
                    state.board[rival_enemy_position_on_board] = 0
                    state.player_1_pos[np.where(state.player_1_pos == rival_enemy_position_on_board)[0][0]] = -2
        else:
            new_soldier_pos, original_index_of_moved_soldier, rival_enemy_position_on_board = move
            state.board[player_pos_list[original_index_of_moved_soldier]] = 0
            state.board[new_soldier_pos] = i
            player_pos_list[original_index_of_moved_soldier] = new_soldier_pos
            if i == 1:
                if rival_enemy_position_on_board != -1:
                    state.board[rival_enemy_position_on_board] = 0
                    state.player_2_pos[np.where(state.player_2_pos == rival_enemy_position_on_board)[0][0]] = -2
            else:
                if rival_enemy_position_on_board != -1:
                    state.board[rival_enemy_position_on_board] = 0
                    state.player_1_pos[np.where(state.player_1_pos == rival_enemy_position_on_board)[0][0]] = -2
        state.turn_number += 1


class BoardUtils:
    @staticmethod
    def count_mills_by_index(board, player_index):
        count = 0
        for indexes in AVAILABLE_MILL_INDEXES:
            board_slice = board[indexes]
            player_indexes_in_slice = np.where(board_slice == player_index)
            curr_sum = board[player_indexes_in_slice].sum()
            if curr_sum == 3 and player_index == 1:
                count += 1
            elif curr_sum == 6 and player_index == 2:
                count += 1
        # print(f'Found {count} CLOSED MILLS')
        # print('board:')
        # printBoard(board)
        return count

    @staticmethod
    def count_pairs_by_index(board, player_index):
        count = 0
        for indexes in AVAILABLE_MILL_INDEXES:
            board_slice = board[indexes]
            pos_indexes = np.where(board_slice == player_index)[0]
            if len(pos_indexes) == 2 and board[indexes].sum() == 2 * player_index:
                count += 1
        return count

    @staticmethod
    def count_3_piece_configs_by_index(board, player_index):
        count = 0
        for config in AVAILABLE_3_PIECES_CONFIGS:
            board_slice = board[config]
            pos_indexes = np.where(board_slice == player_index)[0]
            if len(pos_indexes) == 3 and board[config].sum() == 3 * player_index:
                count += 1
        return count

    @staticmethod
    def count_double_morris_configs_by_index(board, player_index):
        count = 0
        for config in AVAILABLE_3_PIECES_CONFIGS:
            board_slice = board[config]
            pos_indexes = np.where(board_slice == player_index)[0]
            if len(pos_indexes) == 5 and board[config].sum() == 5 * player_index:
                count += 1
        return count


# Stage 1:
# 1. Was mill created in turn (0 if none, 1 if us, -1 if rival) => was_mill_created
# 2. Number of closed mills (our_mills - enemy_mills) in current turn => number_of_closed_mills
# 3. Number of blocked soldiers (rival_blocked - our_blocked) => number_of_blocked_soldiers
# 4. Number of soldiers on board (our_soldiers_count - rival_soldiers_count) => number_of_soldiers_on_board
# 5. diff between soldier pairs (our_pair_count - rival_pair_count) => number_of_pairs
# 6. diff between soldier triplets (our_triplets - rival_triplets) => number_of_3_piece_configs

# Stage 2:
# 1, 2, 3, 4,
# 7. was mill opened in this turn (1 if we opened, 0 if none, -1 if rival) => was_mill_broken
# 8. diff between double triplets (our joined - rival joined) => number_of_double_morris
# 9. is goal state (1 if we won, 0 if no one, -1 if rival) => is_goal


class Heuristics:
    @staticmethod
    def was_mill_created(state):
        for mil_indexes in AVAILABLE_MILL_INDEXES:
            curr_sum = state.board[mil_indexes].sum()
            prev_sum = state.prev_board[mil_indexes].sum()
            if curr_sum == 3 and prev_sum == 2:
                if state.my_index == 1:
                    # we created a mill in this turn
                    return 1
                else:
                    # rival created a mill in this turn
                    return -1
            if curr_sum == 6 and prev_sum == 4:
                if state.my_index == 1:
                    # rival created a mill in this turn
                    return -1
                else:
                    # we created a mill in this turn
                    return 1
        return 0

    @staticmethod
    def was_mill_broken(state):
        for mil_indexes in AVAILABLE_MILL_INDEXES:
            curr_sum = state.board[mil_indexes].sum()
            prev_sum = state.prev_board[mil_indexes].sum()
            if curr_sum == 2 and prev_sum == 3:
                if state.my_index == 1:
                    # we broke a mill in this turn
                    return 1
                else:
                    # rival broke a mill in this turn
                    return -1
            if curr_sum == 4 and prev_sum == 6:
                if state.my_index == 1:
                    # rival broke a mill in this turn
                    return -1
                else:
                    # we broke a mill in this turn
                    return 1
        return 0

    @staticmethod
    def number_of_closed_mills(state):
        res = BoardUtils.count_mills_by_index(state.board, 1) - BoardUtils.count_mills_by_index(state.board, 2)
        if state.my_index == 1:
            return res
        else:
            return -1 * res

    @staticmethod
    def number_of_blocked_soldiers(state):
        res = GameUtils.count_blocked_soldiers_by_player_index(state.board, 2) - \
              GameUtils.count_blocked_soldiers_by_player_index(state.board, 1)
        if state.my_index == 1:
            return res
        else:
            return -1 * res

    @staticmethod
    def number_of_soldiers_on_board(state):
        res = len(GameUtils.get_soldier_position_by_player_index(state.board, 1)) - len(
            GameUtils.get_soldier_position_by_player_index(state.board, 2))
        if state.my_index == 1:
            return res
        else:
            return -1 * res

    @staticmethod
    def number_of_pairs(state):
        res = BoardUtils.count_pairs_by_index(state.board, 1) - BoardUtils.count_pairs_by_index(state.board, 2)
        if state.my_index == 1:
            return res
        else:
            return -1 * res

    @staticmethod
    def number_of_3_piece_configs(state):
        res = BoardUtils.count_3_piece_configs_by_index(state.board, 1) - BoardUtils.count_3_piece_configs_by_index(
            state.board, 2)
        if state.my_index == 1:
            return res
        else:
            return -1 * res

    @staticmethod
    def number_of_double_morris(state):
        res = BoardUtils.count_double_morris_configs_by_index(state.board, 1) - \
              BoardUtils.count_double_morris_configs_by_index(state.board, 2)
        if state.my_index == 1:
            return res
        else:
            return -1 * res

    @staticmethod
    def simple_heuristic(state):
        return len(GameUtils.get_soldier_position_by_player_index(state.board, state.my_index))

    @staticmethod
    def is_goal(state):
        winner_index = GameUtils.return_winner(state)
        if winner_index == 0:
            return 0
        if winner_index == state.my_index:
            return 1
        else:
            return -1


class GameState:
    board: np.array = None
    prev_board = None
    max_time = None
    turn_number = 0
    player_1_pos = np.full(9, -1)
    player_2_pos = np.full(9, -1)
    # Original weights
    # stage_1_h_weights = [18, 26, 1, 6, 18, 7]
    stage_1_h_weights = [50, 26, 30, 30, 30, 7]
    stage_1_h_list = [Heuristics.was_mill_created, Heuristics.number_of_closed_mills,
                      Heuristics.number_of_blocked_soldiers, Heuristics.number_of_soldiers_on_board,
                      Heuristics.number_of_pairs,
                      Heuristics.number_of_3_piece_configs]
    # Original weights
    # stage_2_h_weights = [50, 43, 10, 8, 7, 42, 1086]
    stage_2_h_weights = [50, 43, 30, 30, 8, 8, 100, 30]
    stage_2_h_list = [Heuristics.was_mill_created, Heuristics.number_of_closed_mills,
                      Heuristics.number_of_blocked_soldiers, Heuristics.number_of_soldiers_on_board,
                      Heuristics.was_mill_broken,
                      Heuristics.number_of_double_morris, Heuristics.is_goal, Heuristics.number_of_pairs]

    def __init__(self, board, prev_board, player_1_pos, player_2_pos, turn_number, time_limit, my_index,
                 light_player=False):
        self.board = board
        self.prev_board = prev_board
        self.player_1_pos = player_1_pos
        self.player_2_pos = player_2_pos
        self.turn_number = turn_number
        self.max_time = time_limit
        self.light_player = light_player
        self.my_index = my_index
        if light_player:
            self.stage_1_h_weights = [35]
            self.stage_1_h_list = [Heuristics.number_of_pairs]
            self.stage_2_h_weights = [35]
            self.stage_2_h_list = [Heuristics.number_of_pairs]
