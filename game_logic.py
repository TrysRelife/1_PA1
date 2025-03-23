import math
from ai import minimax, alphabeta, GameState

class Game:
    def __init__(self, settings):
        # Initialize game with settings and default values
        self.current_state = None
        self.bank = 0
        self.algorithm = settings.get('algorithm')  # AI algorithm (minimax or alphabeta)
        self.mode = settings.get('mode')  # Game mode (AI or 1v1)
        self.turn = 1 if settings.get('starting_player') in ['player', 'player1'] else 2  # Starting player
        self.original_turn = self.turn  # Track the original starting player
        self.player1_points, self.player2_points = (0, 0)  # Initialize player scores

    def select_number(self, number):
        # Set the initial game state with the chosen number
        self.current_state = GameState(number, 0, 0, self.bank, self.turn, self.original_turn)

    def make_move(self, divisor):
        # Update the game state based on the chosen divisor (2 or 3)
        if divisor == 2:
            self.current_state = self.current_state.left
        else:
            self.current_state = self.current_state.right
        self.turn = self.current_state.turn  # Update the turn to the next player

    def computer_move(self):
        # Perform a move for the computer using the selected algorithm
        if not self.current_state:
            return None

        depth = 5  # Depth for the search algorithm
        divisor = None

        if self.algorithm == 'alphabeta':
            _, divisor = alphabeta(self.current_state, -math.inf, math.inf, True, 0, depth)
        else:
            _, divisor = minimax(self.current_state, True, 0, depth)

        if divisor is None:
            return None  # No valid move available

        self.make_move(divisor)  # Execute the chosen move
        return divisor  # Return the divisor used

    def get_game_state(self):
        # Return the current game state
        return self.current_state