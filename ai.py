import math

class GameState:
    """
    Represents a specific state of the Number Division Game.
    Includes number, scores, bank, turn, and potential next states.
    """

    def __init__(self, n, cp, pp, b, turn, original_turn):
        """
        Initializes a game state.
        cp: AI/Player 2 score, pp: Human/Player 1 score.
        original_turn: Player who started the game (1 or 2), crucial for heuristic.
        """
        self.n = n
        self.cp = cp
        self.pp = pp
        self.b = b
        self.turn = turn # Player whose turn it is in *this* state
        self.original_turn = original_turn # Who started the game

        # Generate potential child states (next possible moves)
        self.left = self.create_child(2) if n > 1 and n % 2 == 0 else None
        self.right = self.create_child(3) if n > 1 and n % 3 == 0 else None

        # A state is terminal if no further moves are possible
        self._is_terminal = (n <= 1) or (self.left is None and self.right is None)

        # Calculate heuristic value upon initialization
        self.h = self.heuristic()

    def create_child(self, divisor):
        """Generates a successor game state resulting from dividing by the divisor."""
        new_n = self.n // divisor
        pt = 1 if new_n % 2 == 0 else -1 # Points for this move (+1 if new_n even, -1 if odd)

        # Assign points to the player *making* the current move (self.turn)
        new_cp_add = pt if self.turn == 2 else 0
        new_pp_add = pt if self.turn == 1 else 0

        new_cp = max(0, self.cp + new_cp_add)
        new_pp = max(0, self.pp + new_pp_add)
        new_b = self.b + (1 if new_n % 5 == 0 else 0) # Update bank if new_n divisible by 5

        # Determine whose turn it is in the *next* state
        new_turn = None
        is_new_state_terminal = (new_n <= 1) or (new_n % 2 != 0 and new_n % 3 != 0)
        if not is_new_state_terminal:
             new_turn = 2 if self.turn == 1 else 1 # Switch turns

        return GameState(new_n, new_cp, new_pp, new_b, new_turn, self.original_turn)

    def terminal(self):
        """Checks if the current game state represents the end of the game."""
        return self._is_terminal

    def heuristic(self):
        """
        Estimates the value of the state for the player who started the game (original_turn).
        Higher value is better for the starting player.
        ALIGNED WITH WINNER DETERMINATION (scores only in terminal state).
        """
        # --- Terminal State Evaluation ---
        if self.terminal():
            # Final value based *only* on score difference, aligned with determine_winner()
            score_diff = (self.pp - self.cp) if self.original_turn == 1 else (self.cp - self.pp)
            # Return a large value if winning, small if losing, to make terminal states dominant
            if score_diff > 0: return 1000.0 + score_diff # Win for original starter
            elif score_diff < 0: return -1000.0 + score_diff # Loss for original starter
            else: return 0.0 # Draw

        # --- Non-Terminal State Evaluation Weights ---
        W_SCORE_DIFF = 1.0    # Base weight for current score difference
        W_BANK = 0.05         # *** Bank is very secondary - reduced weight ***
        W_IMMEDIATE_POINTS = 0.8 # Weight for points from *our* next move
        W_MOVE_OPTIONS = 0.05 # Small bonus for flexibility

        # --- Calculate Base Value ---
        score_diff = (self.pp - self.cp) if self.original_turn == 1 else (self.cp - self.pp)
        # Include bank with very low weight, might even set W_BANK to 0
        heuristic_val = (W_SCORE_DIFF * score_diff) + (W_BANK * self.b)

        # --- Calculate Immediate Point Potential ---
        possible_points = []
        if self.left:
            possible_points.append(1 if (self.n // 2) % 2 == 0 else -1)
        if self.right:
            possible_points.append(1 if (self.n // 3) % 2 == 0 else -1)

        if possible_points:
            best_potential_pts = max(possible_points) # Best outcome for current player

            # Adjust heuristic based on whose turn it is
            if self.turn == self.original_turn: # Good if starter has good move
                heuristic_val += W_IMMEDIATE_POINTS * best_potential_pts
            else: # Bad if opponent has good move (subtract their best potential)
                heuristic_val -= W_IMMEDIATE_POINTS * best_potential_pts

        # --- Add small bonus for Move Options ---
        move_count = len(possible_points)
        if move_count > 0:
            heuristic_val += W_MOVE_OPTIONS * (move_count / 2.0)

        return heuristic_val


def minimax(state, depth, maximizing, max_depth=10):
    nodes_explored = 1
    if state.terminal() or depth >= max_depth:
        return (state.h, None, nodes_explored)

    moves = []
    if state.left: moves.append((state.left, 2))
    if state.right: moves.append((state.right, 3))
    if not moves: return (state.h, None, nodes_explored)
    best_move = moves[0][1]
    if maximizing:
        max_val = -math.inf
        for child, move in moves:
            # Pass max_depth down correctly
            child_val, _, child_nodes = minimax(child, depth + 1, False, max_depth)
            nodes_explored += child_nodes
            if child_val > max_val:
                max_val = child_val
                best_move = move
            elif child_val == max_val and move == 3:
                 best_move = move
        return (max_val, best_move, nodes_explored)
    else:
        min_val = math.inf
        for child, move in moves:
            # Pass max_depth down correctly
            child_val, _, child_nodes = minimax(child, depth + 1, True, max_depth)
            nodes_explored += child_nodes
            if child_val < min_val:
                min_val = child_val
                best_move = move
            elif child_val == min_val and move == 2:
                 best_move = move
        return (min_val, best_move, nodes_explored)


def alphabeta(state, depth, alpha, beta, maximizing, max_depth=10):
    nodes_explored = 1
    if state.terminal() or depth >= max_depth:
        return (state.h, None, nodes_explored)

    moves = []
    if state.left: moves.append((state.left, 2))
    if state.right: moves.append((state.right, 3))
    if not moves: return (state.h, None, nodes_explored)
    best_move = moves[0][1]
    if maximizing:
        value = -math.inf
        for child, move in moves:
             # Pass max_depth down correctly
            child_val, _, child_nodes = alphabeta(child, depth + 1, alpha, beta, False, max_depth)
            nodes_explored += child_nodes
            if child_val > value:
                value = child_val
                best_move = move
            elif child_val == value and move == 3:
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (value, best_move, nodes_explored)
    else: # Minimizing
        value = math.inf
        for child, move in moves:
             # Pass max_depth down correctly
            child_val, _, child_nodes = alphabeta(child, depth + 1, alpha, beta, True, max_depth)
            nodes_explored += child_nodes
            if child_val < value:
                value = child_val
                best_move = move
            elif child_val == value and move == 2:
                 best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (value, best_move, nodes_explored)