import math
import time # To time AI calculations
# Assuming ai.py now contains the versions WITHOUT depth limit
from ai import minimax, alphabeta, GameState

class Game:
    """Manages the game flow, state transitions, and AI interaction."""

    def __init__(self, settings):
        """Initializes the game based on user settings."""
        self.settings = settings
        self.current_state = None # Holds the current GameState object
        self.algorithm = settings.get('algorithm') # 'minimax' or 'alphabeta'
        self.mode = settings.get('mode') # 'AI' or '1v1'
        # Determine the first player (1 for player/player1, 2 for ai/player2)
        self.turn = 1 if settings.get('starting_player') in ['player', 'player1'] else 2
        self.original_turn = self.turn # Store who started for consistent AI evaluation
        self.initial_number = 0
        # Statistics
        self.total_moves = 0
        self.total_ai_time = 0.0
        self.total_nodes_explored = 0
        self.winner = None # To store winner ('Player', 'AI', 'Player 1', 'Player 2', 'Draw')
        self.starting_player = settings.get('starting_player')

    def select_number(self, number):
        """Sets the starting number and creates the initial game state."""
        self.initial_number = number
        # Create the root GameState
        self.current_state = GameState(number, 0, 0, 0, self.turn, self.original_turn)
        # Reset game statistics
        self.total_moves = 0
        self.total_ai_time = 0.0
        self.total_nodes_explored = 0
        self.winner = None

    def make_move(self, divisor):
        """Applies a move (dividing by 2 or 3) to the current game state."""
        next_state = None
        # Retrieve the pre-calculated child state corresponding to the divisor
        if divisor == 2 and self.current_state.left:
            next_state = self.current_state.left
        elif divisor == 3 and self.current_state.right:
            next_state = self.current_state.right

        self.current_state = next_state # Update the game state
        self.total_moves += 1
        # Update whose turn it is based on the new state (could be None if terminal)
        self.turn = self.current_state.turn

        if self.current_state.terminal(): # Check if the game ended
            self.determine_winner()

    def computer_move(self):
        """Calculates and performs the AI's move using unlimited depth search."""
        if not self.current_state or self.current_state.terminal():
            return None # No move if game over or not started

        # Determine if the AI is the maximizing player from the heuristic's perspective
        is_maximizing_perspective = (self.turn == self.original_turn)

        # No depth limit parameters needed for the calls anymore
        # depth = 8 # REMOVED - No longer used
        divisor = None
        nodes = 0
        start_time = time.perf_counter() # Start timing

        print(f"AI ({self.algorithm}) thinking from N={self.current_state.n}...") # Add thinking message

        # --- MODIFIED CALLS ---
        if self.algorithm == 'alphabeta':
            # Call alphabeta without depth/max_depth
            _, divisor, nodes = alphabeta(self.current_state, -math.inf, math.inf, is_maximizing_perspective)
        else: # Default to minimax
            # Call minimax without depth/max_depth
            _, divisor, nodes = minimax(self.current_state, is_maximizing_perspective)
        # --- END MODIFIED CALLS ---

        # Record performance statistics
        move_time = time.perf_counter() - start_time
        self.total_ai_time += move_time
        self.total_nodes_explored += nodes
        print(f"AI calculation took: {move_time:.4f}s, explored {nodes:,} nodes.") # Add timing/node info

        # Check if a valid move was found
        if divisor is None:
            # This might happen if the AI is called on a state mistakenly thought non-terminal
            print(f"Warning: AI could not find a move for N={self.current_state.n}. State terminal: {self.current_state.terminal()}")
            if not self.current_state.terminal():
                 self.determine_winner() # Ensure winner is determined if game should have ended
            return None

        print(f"AI chooses to divide by {divisor}") # Announce AI move
        self.make_move(divisor) # Apply the AI's chosen move
        return divisor # Return the divisor used

    def get_game_state(self):
        """Returns the current GameState object."""
        return self.current_state

    def determine_winner(self):
        """Determines the winner based on the final scores in the terminal state."""
        if self.winner is not None: return # Avoid re-determining

        state = self.current_state
        # Check if state is valid before accessing attributes
        if not state:
            print("Error: Trying to determine winner with no game state.")
            self.winner = "Error"
            return

        # Get final scores mapped correctly to Player 1 and Player 2 based on who started
        # This part correctly identifies P1/P2 scores regardless of start
        p1_score = state.pp if state.original_turn == 1 else state.cp
        p2_score = state.cp if state.original_turn == 1 else state.pp

        # Determine winner based on score comparison
        if p1_score > p2_score:
            winner_label = "Player 1"
        elif p2_score > p1_score:
            winner_label = "Player 2"
        else: # Scores are equal
            winner_label = "Draw"

        # Adjust labels for 'AI' mode vs '1v1' mode
        if self.mode == 'AI':
            is_p1_human = (state.original_turn == 1) # True if human started as P1

            if winner_label == "Player 1":
                # If P1 won, check if P1 was the human or the AI
                self.winner = "Player" if is_p1_human else "AI"
            elif winner_label == "Player 2":
                # If P2 won, check if P2 was the AI or the human
                self.winner = "AI" if is_p1_human else "Player"
            else: # Draw
                self.winner = "Draw"
        else: # 1v1 mode uses 'Player 1' / 'Player 2'
            self.winner = winner_label