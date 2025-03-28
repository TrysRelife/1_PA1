import math

class GameState:
    """Represents the state of the Number Division Game at a specific point."""

    def __init__(self, n, cp, pp, b, turn, original_turn):
        """
        Initialize a game state.
        n: Current number.
        cp: AI/Player 2 score.
        pp: Human/Player 1 score.
        b: Bank value.
        turn: Player whose turn it is (1 or 2).
        original_turn: Player who started the game (1 or 2).
        """
        self.n = n
        self.cp = cp
        self.pp = pp
        self.b = b
        self.turn = turn
        self.original_turn = original_turn # Used for consistent heuristic evaluation

        # Generate potential child states (next possible moves)
        # Division requires n > 3.
        self.left = self.create_child(2) if n > 3 and n % 2 == 0 else None
        self.right = self.create_child(3) if n > 3 and n % 3 == 0 else None

        # A state is terminal if no further moves are possible (n <= 3)
        self._is_terminal = self.left is None and self.right is None

        # Calculate the heuristic value ONLY if it's terminal.
        # Value for non-terminal states isn't needed for the base case here.
        self.h = self.heuristic() if self._is_terminal else 0 # Assign 0 or other placeholder if not terminal

    def create_child(self, divisor):
        """Generates a successor game state after dividing by the divisor."""
        new_n = self.n // divisor
        # Points awarded: +1 if the new number is even, -1 if odd
        pt = 1 if new_n % 2 == 0 else -1

        # Assign points to the player whose turn it is in the *current* state
        new_cp_add = pt if self.turn == 2 else 0
        new_pp_add = pt if self.turn == 1 else 0

        # Update scores (cannot go below 0)
        new_cp = max(0, self.cp + new_cp_add)
        new_pp = max(0, self.pp + new_pp_add)
        # Update bank if the new number is divisible by 5
        new_b = self.b + (1 if new_n % 5 == 0 else 0) # Bank still updated, though ignored by heuristic

        # Determine whose turn it is in the next state
        new_turn = None
        # Check if the *new* state will be terminal (n <= 3)
        is_new_state_terminal = (new_n <= 3)
        if not is_new_state_terminal:
             new_turn = 2 if self.turn == 1 else 1 # Switch turns

        return GameState(new_n, new_cp, new_pp, new_b, new_turn, self.original_turn)

    def terminal(self):
        """Returns true if this state is a terminal state (no more moves)."""
        return self._is_terminal

    def heuristic(self):
        """
        Evaluates the value of a TERMINAL state for the player who started the game.
        Higher value is better for the starting player.
        """
        # Calculate score difference from the perspective of the original starting player
        score_diff = (self.pp - self.cp) if self.original_turn == 1 else (self.cp - self.pp)

        # Return large values indicating win/loss/draw for the starting player
        # (Adding score_diff helps slightly in tie-breaking between win/loss states if needed)
        if score_diff > 0: return 1000.0 + score_diff # Win for original starter
        elif score_diff < 0: return -1000.0 + score_diff # Loss for original starter
        else: return 0.0 # Draw


# --- Minimax Algorithm (Unlimited Depth) ---
def minimax(state, maximizing):
    """
    Performs the minimax search algorithm WITHOUT depth limit.
    Returns (best_value, best_move_divisor, nodes_explored).
    WARNING: Can be extremely slow or run indefinitely for large N.
    """
    nodes_explored = 1
    # Base case: ONLY stop at actual terminal game states
    if state.terminal():
        # Use the heuristic value calculated specifically for terminal states
        return (state.h, None, nodes_explored)

    # Get available moves
    moves = []
    if state.left: moves.append((state.left, 2))
    if state.right: moves.append((state.right, 3))

    best_move = moves[0][1] # Default to the first available move

    if maximizing:
        max_val = -math.inf
        for child, move in moves:
            # Recursive call - NO depth parameter passed
            child_val, _, child_nodes = minimax(child, False) # Switch to minimizing
            nodes_explored += child_nodes
            # Update max value and best move
            if child_val > max_val:
                max_val = child_val
                best_move = move
            # Tie-breaking: Prefer dividing by 3 if values are equal
            elif child_val == max_val and move == 3:
                 best_move = move
        return (max_val, best_move, nodes_explored)
    else: # Minimizing
        min_val = math.inf
        for child, move in moves:
            # Recursive call - NO depth parameter passed
            child_val, _, child_nodes = minimax(child, True) # Switch to maximizing
            nodes_explored += child_nodes
            # Update min value and best move
            if child_val < min_val:
                min_val = child_val
                best_move = move
            # Tie-breaking: Prefer dividing by 2 if values are equal
            elif child_val == min_val and move == 2:
                 best_move = move
        return (min_val, best_move, nodes_explored)


# --- Alpha-Beta Algorithm (Unlimited Depth) ---
def alphabeta(state, alpha, beta, maximizing):
    """
    Performs minimax search with alpha-beta pruning WITHOUT depth limit.
    Returns (best_value, best_move_divisor, nodes_explored).
    WARNING: Can be extremely slow or run indefinitely for large N.
    """
    nodes_explored = 1
    # Base case: ONLY stop at actual terminal game states
    if state.terminal():
        # Use the heuristic value calculated specifically for terminal states
        return (state.h, None, nodes_explored)

    # Get available moves
    moves = []
    if state.left: moves.append((state.left, 2))
    if state.right: moves.append((state.right, 3))

    best_move = moves[0][1] # Default best move

    if maximizing:
        value = -math.inf
        # Consider move order for potentially better pruning (e.g., evaluate preferred tie-break move first?)
        # Simple iteration here:
        for child, move in moves:
            # Recursive call - NO depth parameter passed
            child_val, _, child_nodes = alphabeta(child, alpha, beta, False) # Switch to minimizing
            nodes_explored += child_nodes

            # Update the best value found so far for this maximizing node
            if child_val > value:
                value = child_val
                best_move = move # Update best move only when value improves
            # Tie-breaking: Prefer 3
            elif child_val == value and move == 3:
                best_move = move

            # --- Pruning Check ---
            if value >= beta: # Check if current best value is already too high for the MIN parent
                break # Beta cut-off
            # --- Update Alpha ---
            alpha = max(alpha, value) # Update the best option found for MAX along this path

        return (value, best_move, nodes_explored)

    else: # Minimizing
        value = math.inf
        # Consider move order for potentially better pruning
        for child, move in moves:
            # Recursive call - NO depth parameter passed
            child_val, _, child_nodes = alphabeta(child, alpha, beta, True) # Switch to maximizing
            nodes_explored += child_nodes

            # Update the best value found so far for this minimizing node
            if child_val < value:
                value = child_val
                best_move = move # Update best move only when value improves
            # Tie-breaking: Prefer 2
            elif child_val == value and move == 2:
                 best_move = move

            # --- Pruning Check ---
            if value <= alpha: # Check if current best value is already too low for the MAX parent
                break # Alpha cut-off
            # --- Update Beta ---
            beta = min(beta, value) # Update the best option found for MIN along this path

        return (value, best_move, nodes_explored)
