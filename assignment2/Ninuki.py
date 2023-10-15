#!/usr/bin/python3

"""
Go0 random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller
"""

import time
from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine

class Go0(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, "Go0", 1.0)
        self.time_limit = 1  # Default time limit is 1 second

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color, use_eye_filter=False)
    
    def set_time_limit(self, seconds: int) -> None:
        self.time_limit = seconds
    
    def solve(self, board: GoBoard) -> str:
        color = self._get_color_to_play(board)
        start_time = time.time()
        best_move, result = self._minimax_solve(board, color, start_time)
        
        if time.time() - start_time > self.time_limit or result == "unknown":
            return "unknown"
        
        if result == 0:
            return f"draw {best_move}"
        
        elif result == 1:
            return f"b {best_move}"
        
        elif result == -1:
            return f"w {best_move}"
        
    def _minimax_solve(self, board: GoBoard, color: GO_COLOR, start_time: float, depth=0) -> tuple:
        if time.time() - start_time > self.time_limit:
            return None, "unknown"
        
        legal_moves = GoBoardUtil.generate_legal_moves(board, color)
        if not legal_moves:
            return None, "unknown"
        
        best_move = None
        best_score = -float('inf') if color == 1 else float('inf')
        
        for move in legal_moves:
            board.play_move(move, color)
            _, score = self._minimax_solve(board, 3 - color, start_time, depth+1)
            board.undo_move()
            
            if score == "unknown":  # Handling unknown score explicitly
                continue
            
            if color == 1 and score > best_score:
                best_score = score
                best_move = move
            elif color == 2 and score < best_score:
                best_score = score
                best_move = move
        
        if best_move is None:  # If no valid move found, return unknown
            return None, "unknown"
        
        return best_move, best_score

    
    def _get_color_to_play(self, board: GoBoard) -> GO_COLOR:
        board_size = board.get_size()
        black_count = 0
        white_count = 0
        for row in range(board_size):
            for col in range(board_size):
                 position = board._coord_to_point(row+1, col+1)
                 color = board.get_color(position)
                 if color == 1:
                     black_count += 1
                 elif color == 2:
                     white_count += 1
                
        return 1 if black_count <= white_count else 2

def run() -> None:
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(Go0(), board)
    con.start_connection()

if __name__ == "__main__":
    run()
