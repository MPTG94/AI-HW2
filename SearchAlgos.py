"""Search Algos: MiniMax, AlphaBeta
"""
# TODO: you can import more modules, if needed
# DONE TODO: update ALPHA_VALUE_INIT, BETA_VALUE_INIT in utils
import time
import numpy as np
from utils import GameUtils
from copy import deepcopy

ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf  # !!!!!


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
        raise NotImplementedError
