import math
import time # For timing AI calculations
from ai import minimax, alphabeta, GameState

class Game:
    """
    Handles the overall game flow, state management, player turns,
    and AI decision-making.
    """

    def __init__(self, settings):
        """Initializes the game based on settings from the main menu."""
        self.settings = settings
        self.current_state = None
        self.algorithm = settings.get('algorithm')
        self.mode = settings.get('mode')
        # Turn: 1 for player/player1, 2 for ai/player2
        self.turn = 1 if settings.get('starting_player') in ['player', 'player1'] else 2
        self.original_turn = self.turn # Store who started for AI evaluation
        self.initial_number = 0
        self.total_moves = 0
        self.total_ai_time = 0.0 # Statistics for AI performance
        self.total_nodes_explored = 0
        self.winner = None # 'Player', 'AI', 'Player 1', 'Player 2', 'Draw'
        self.starting_player = settings.get('starting_player')

    def select_number(self, number):
        """Sets up the initial game state with the chosen starting number."""
        self.initial_number = number
        # Create the root GameState
        self.current_state = GameState(number, 0, 0, 0, self.turn, self.original_turn)
        # Reset stats
        self.total_moves = 0
        self.total_ai_time = 0.0
        self.total_nodes_explored = 0
        self.winner = None

    def make_move(self, divisor):
        """Applies a division move to the current game state, updating it."""
        next_state = None
        # Find the pre-calculated child state for the move
        if divisor == 2 and self.current_state.left:
            next_state = self.current_state.left
        elif divisor == 3 and self.current_state.right:
            next_state = self.current_state.right

        if next_state:
            self.current_state = next_state # Advance state
            self.total_moves += 1
            self.turn = self.current_state.turn # Update whose turn it is

            if self.current_state.terminal(): # Check for game end
                self.determine_winner()
        else:
            # Should not happen if UI is correct
            print(f"Warning: Invalid move attempted ({divisor}) for N={self.current_state.n}")

    def computer_move(self):
        """Calculates and performs the AI's move using the selected algorithm."""
        if not self.current_state or self.current_state.terminal():
            return None

        # AI perspective aligns with the original starter for minimax/alphabeta evaluation
        is_maximizing_perspective = (self.turn == self.original_turn)

        depth = 8 # AI search depth
        divisor = None
        nodes = 0
        start_time = time.perf_counter() # Time the AI calculation

        if self.algorithm == 'alphabeta':
            _, divisor, nodes = alphabeta(self.current_state, 0, -math.inf, math.inf, is_maximizing_perspective, depth)
        else: # Default to minimax
            _, divisor, nodes = minimax(self.current_state, 0, is_maximizing_perspective, depth)

        move_time = time.perf_counter() - start_time
        self.total_ai_time += move_time
        self.total_nodes_explored += nodes

        if divisor is None:
            print(f"Warning: AI could not find a move for N={self.current_state.n}. State terminal: {self.current_state.terminal()}")
            if not self.current_state.terminal():
                 self.determine_winner()
            return None

        self.make_move(divisor) # Apply the chosen move
        return divisor

    def get_game_state(self):
        """Provides access to the current game state object."""
        return self.current_state

    def determine_winner(self):
        """Determines the winner based on final scores and bank."""
        if self.winner is not None: return # Already determined

        state = self.current_state
        # Get final scores mapped to P1/P2 based on who started
        p1_score = state.pp if state.original_turn == 1 else state.cp
        p2_score = state.cp if state.original_turn == 1 else state.pp

        # Winner based on score difference + bank (bank considered neutral here for simplicity, winner determined by scores)
        # Simplified check: compare scores directly first, then consider bank maybe?
        # The heuristic adds bank, so let's align winner check with that idea implicitly.
        # Who gets the bank depends on heuristic definition, assume P1 for now in heuristic.
        # For winner determination, just compare scores.
        if p1_score > p2_score:
            winner_label = "Player 1"
        elif p2_score > p1_score:
            winner_label = "Player 2"
        else: # Scores are equal, it's a draw
            winner_label = "Draw"

        # Remap winner labels for 'AI' mode
        if self.mode == 'AI':
            if winner_label == "Player 1": self.winner = "Player"
            elif winner_label == "Player 2": self.winner = "AI"
            else: self.winner = "Draw"
        else: # 1v1 mode
            self.winner = winner_label