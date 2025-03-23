import math

class GameState:
    def __init__(self, n, cp, pp, b, turn, original_turn):
        # Initialize game state with current number, scores, bonus, and turn
        self.n = n
        self.cp = cp
        self.pp = pp
        self.b = b
        self.turn = turn
        self.original_turn = original_turn

        # Precompute child states for possible moves (divide by 2 or 3)
        self.left = self.create_child(2) if n % 2 == 0 else None
        self.right = self.create_child(3) if n % 3 == 0 else None
        self.h = self.heuristic()

    def create_child(self, divisor):
        # Create a new state by dividing the current number by the divisor
        new_n = self.n // divisor
        pt = 1 if new_n % 2 == 0 else -1  # Bonus if new_n is even, penalty otherwise

        # Update scores based on the current player's turn
        new_cp = self.cp + (pt if self.turn != self.original_turn else 0)
        new_pp = self.pp + (pt if self.turn == self.original_turn else 0)
        new_cp = max(new_cp, 0)  # Ensure scores don't go negative
        new_pp = max(new_pp, 0)

        # Increase bonus if new_n is divisible by 5
        new_b = self.b + (1 if new_n % 5 == 0 else 0)

        # Determine the next turn if moves are still possible
        new_turn = None
        if new_n % 2 == 0 or new_n % 3 == 0:
            new_turn = 2 if self.turn == 1 else 1

        return GameState(new_n, new_cp, new_pp, new_b, new_turn, self.original_turn)

    def terminal(self):
        # Check if the game has reached a terminal state
        return self.turn is None

    def heuristic(self):
        # Calculate the heuristic score based on scores, bonus, and whether the number is even
        if self.original_turn == 2:
            return (self.cp - self.pp) + self.b + (1 if self.n % 2 == 0 else 0)
        else:
            return (self.pp - self.cp) + self.b + (1 if self.n % 2 == 0 else 0)


def minimax(state, depth, maximizing, max_depth=10):
    # Minimax algorithm to determine the best move
    if state.terminal() or depth >= max_depth:
        return (state.h, None)  # Return heuristic value and no move at terminal state

    moves = []
    # Prioritize division by 3 by considering the right child first
    if state.right:
        moves.append((state.right, 3))
    if state.left:
        moves.append((state.left, 2))

    if maximizing:
        max_val = -math.inf
        best_move = None

        for child, move in moves:
            child_val, _ = minimax(child, depth + 1, False, max_depth)

            # Update best move if child's value is higher, or equal with priority for move 3
            if child_val > max_val or (child_val == max_val and move == 3):
                max_val = child_val
                best_move = move

        return (max_val, best_move)

    else:  # Minimizing player
        min_val = math.inf
        best_move = None

        for child, move in moves:
            child_val, _ = minimax(child, depth + 1, True, max_depth)

            # Update best move if child's value is lower, or equal with priority for move 2
            if child_val < min_val or (child_val == min_val and move == 2):
                min_val = child_val
                best_move = move

        return (min_val, best_move)


def alphabeta(state, depth, alpha, beta, maximizing, max_depth=10):
    # Alpha-beta pruning algorithm to optimize minimax
    if state.terminal() or depth >= max_depth:
        return (state.h, None)  # Return heuristic value and no move at terminal state

    moves = []
    # Prioritize division by 3 by considering the right child first
    if state.right:
        moves.append((state.right, 3))
    if state.left:
        moves.append((state.left, 2))

    if maximizing:
        value = -math.inf
        best_move = None

        for child, move in moves:
            child_val, _ = alphabeta(child, depth + 1, alpha, beta, False, max_depth)

            # Update best move if child's value is higher, or equal with priority for move 3
            if child_val > value or (child_val == value and move == 3):
                value = child_val
                best_move = move

            alpha = max(alpha, value)
            if beta <= alpha:
                break  # Beta cutoff

    else:  # Minimizing player
        value = math.inf
        best_move = None

        for child, move in moves:
            child_val, _ = alphabeta(child, depth + 1, alpha, beta, True, max_depth)

            # Update best move if child's value is lower, or equal with priority for move 2
            if child_val < value or (child_val == value and move == 2):
                value = child_val
                best_move = move

            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cutoff

    return (value, best_move)