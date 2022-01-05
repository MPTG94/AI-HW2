import operator
import numpy as np
import os

# TODO: edit the alpha and beta initialization values for AlphaBeta algorithm.
# instead of 'None', write the real initialization value, learned in class.
# hint: you can use np.inf
ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf


def get_directions(position):
    """Returns all the possible directions of a player in the game as a list.
    """
    assert 0 <= position <= 23, "illegal move"
    adjacent = [
        [1, 3],
        [0, 2, 9],
        [1, 4],
        [0, 5, 11],
        [2, 7, 12],
        [3, 6],
        [5, 7, 14],
        [4, 6],
        [9, 11],
        [1, 8, 10, 17],
        [9, 12],
        [3, 8, 13, 19],
        [4, 10, 15, 20],
        [11, 14],
        [6, 13, 15, 22],
        [12, 14],
        [17, 19],
        [9, 16, 18],
        [17, 20],
        [11, 16, 21],
        [12, 18, 23],
        [19, 22],
        [21, 23, 14],
        [20, 22]
    ]
    return adjacent[position]


# def tup_add(t1, t2):
#     """
#     returns the sum of two tuples as tuple.
#     """
#     return tuple(map(operator.add, t1, t2))

def printBoard(board):
    print(int(board[0]), "(00)-----------------------", int(board[1]), "(01)-----------------------", int(board[2]),
          "(02)")
    print("|                             |                             |")
    print("|                             |                             |")
    print("|                             |                             |")
    print("|       ", int(board[8]), "(08)--------------", int(board[9]), "(09)--------------", int(board[10]),
          "(10)   |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       |        ", int(board[16]), "(16)-----", int(board[17]), "(17)-----", int(board[18]),
          "(18)   |        |")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print(int(board[3]), "(03)-", int(board[11]), "(11)---", int(board[19]), "(19)                 ",
          int(board[20]), "(20)-", int(board[12]), "(12)---", int(board[4]), "(04)")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print("|       |        ", int(board[21]), "(21)-----", int(board[22]), "(22)-----", int(board[23]),
          "(23)   |        |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       ", int(board[13]), "(13)--------------", int(board[14]), "(14)--------------", int(board[15]),
          "(15)   |")
    print("|                             |                             |")
    print("|                             |                             |")
    print("|                             |                             |")
    print(int(board[5]), "(05)-----------------------", int(board[6]), "(06)-----------------------", int(board[7]),
          "(07)")
    print("\n")


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
        for position, soldier in enumerate(positions):
            if soldier == player_index:
                moves = get_directions(position)
                for move in moves:
                    if board[move] == 0:
                        num_moves += 1
        return num_moves

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
    def check_winner_by_player_index(board, player_index):
        """
        Checks the win conditions
        :param board: the board
        :param player_index: the player to check if he won
        :return: True if the player won, False otherwise
        """
        if player_index == 1:
            if not GameUtils.can_player_i_move(board, 2) or GameUtils.count_soldiers_by_player_index(board, 2) < 3:
                return True
            return False
        else:
            if not GameUtils.can_player_i_move(board, 1) or GameUtils.count_soldiers_by_player_index(board, 1) < 3:
                return True
            return False

    @staticmethod
    def return_winner(board):
        if GameUtils.check_winner_by_player_index(board, 1):
            return 1
        elif GameUtils.check_winner_by_player_index(board, 2):
            return 2
        return 0

    @staticmethod
    def check_goal(board):
        return GameUtils.return_winner(board) > 0

    @staticmethod
    def successor_func(board, i):
        pass
        # Need to figure out what the successor function is, my guess is it needs to check for the next available moves of every soldier, and
        # find out what is the best one (going to some depth I guess)

    @staticmethod
    def utility_method(board, i):
        pass
        # Need to figure out a good utility method, supposedly it should check who won, and who is checking,
        # and return a numerical value accordingly, similar to tutorials definition


# TODO: do we want a game state class which stores many parameters (board, player 1 pos, player 2 pos, etc..)?