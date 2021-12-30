from players.AbstractPlayer import AbstractPlayer
import numpy as np
import random

class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.board = None  # and add two more fields to Player
        self.my_pos = None
        self.rival_pos = None
        self.turn = 0

    def set_game_params(self, board):
        self.board = board
        self.my_pos = np.full(9, -1)
        self.rival_pos = np.full(9, -1)
        self.turn = 0

    def make_move(self, time_limit) -> tuple:  # time parameter is not used, we assume we have enough time.
        # print("Simple player: turn:", self.turn) # !!!

        if self.turn < 18:
            move = self._stage_1_move()
            self.turn += 1
            return move

        else:
            move = self._stage_2_move()
            self.turn += 1
            # self.print_player_board()
            return move

    def set_rival_move(self, move):
        rival_pos, rival_soldier, my_dead_pos = move

        if self.turn < 18:
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        else:
            rival_prev_pos = self.rival_pos[rival_soldier]
            self.board[rival_prev_pos] = 0
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        if my_dead_pos != -1:
            self.board[my_dead_pos] = 0
            dead_soldier = int(np.where(self.my_pos == my_dead_pos)[0][0])
            self.my_pos[dead_soldier] = -2
        self.turn += 1

    def _update_player_on_board(self, next_pos, prev_pos, soldier):
        # update position and board:
        self.board[next_pos] = 1
        self.board[prev_pos] = 0
        self.my_pos[soldier] = next_pos

    def _choose_rival_cell_to_kill(self):
        rival_cell = int(np.random.choice(np.where(self.board == 2)[0], 1)[0]) # choose random cell
        return rival_cell

    def _make_mill_get_rival_cell(self):
        rival_cell = self._choose_rival_cell_to_kill()
        rival_idx = np.where(self.rival_pos == rival_cell)[0][0]
        self.rival_pos[rival_idx] = -2
        self.board[rival_cell] = 0
        return rival_cell

    def _stage_1_choose_cell_and_soldier_to_move(self):
        cell = int(np.random.choice(np.where(self.board == 0)[0], 1)[0]) # choose random cell
        soldier_that_moved = int(np.random.choice(np.where(self.my_pos == -1)[0], 1)[0]) # choose random soldier
        return cell, soldier_that_moved

    def _stage_1_move(self) -> tuple:
        cell, soldier_that_moved = self._stage_1_choose_cell_and_soldier_to_move()
        self.my_pos[soldier_that_moved] = cell
        self.board[cell] = 1

        rival_cell = -1 if not self.is_mill(cell) else self._make_mill_get_rival_cell()
        return cell, soldier_that_moved, rival_cell

    def _stage_2_move(self) -> tuple:
        direction, soldier_that_moved = -1, -1

        while True:
            # choose random soldier_on_board to move
            soldier_cell = int(np.random.choice(np.where(self.board == 1)[0], 1)[0])
            # check if can move
            direction_list = self.directions(int(soldier_cell))
            valid_direction = [direction for direction in direction_list if self.board[direction] == 0]
            if len(valid_direction) == 0:
                continue
            direction = random.choice(valid_direction)
            soldier_that_moved = int(np.where(self.my_pos == soldier_cell)[0][0])
            self._update_player_on_board(direction, self.my_pos[soldier_that_moved], soldier_that_moved)
            # check if made mill
            rival_cell = -1 if not self.is_mill(direction) else self._make_mill_get_rival_cell()

            return direction, soldier_that_moved, rival_cell

        assert direction == -1, 'No moves'

    def _print_player_board(self):
        print("board:")
        print(self.board)
        print(np.arange(24))

        print("my pos:")
        print(self.my_pos)
        print(np.arange(9))