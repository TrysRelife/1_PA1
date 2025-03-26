import customtkinter as ctk
import re # Import regular expressions module for name conversion
from gui.main_menu import MainMenu
from gui.game_screen import GameScreen
from gui.result_screen import ResultScreen
from gui.high_score_screen import HighScoreScreen
from game_logic import Game
import score_manager

class GameApp(ctk.CTk):
    """
    The main application class controlling UI frames and game logic instance.
    """
    def __init__(self):
        """Initializes the main application window and frames."""
        super().__init__()
        self.title("Number Division Game")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.current_frame = None # Currently displayed frame
        self.game = None          # Active Game logic instance

        # Create instances of all UI frames (screens)
        self.frames = {}
        for F in (MainMenu, GameScreen, ResultScreen, HighScoreScreen):
            # Convert CamelCase class name (e.g., HighScoreScreen)
            # to snake_case (e.g., high_score_screen) for the key.
            name = F.__name__
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            frame_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

            frame = F(controller=self)
            self.frames[frame_name] = frame
            # --- Debugging Print: Check registered frame names ---
            print(f"Registered frame with key: '{frame_name}'")
            # --- End Debugging Print ---


        self.show_frame("main_menu") # Show the main menu initially

    def show_frame(self, frame_name):
        """Hides the current frame and displays the specified frame."""
        new_frame = self.frames.get(frame_name)
        if not new_frame:
            # --- Error Print ---
            print(f"Error: Frame '{frame_name}' not found. Available frames: {list(self.frames.keys())}")
            return

        if self.current_frame:
            self.current_frame.pack_forget() # Hide current frame

        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True) # Show new frame

        # Call 'on_show' for frame-specific setup/refresh logic
        if hasattr(self.current_frame, "on_show"):
            self.current_frame.on_show()

    def start_new_game(self, settings, starting_number):
        """Initializes a new game session and switches to the game screen."""
        self.game = Game(settings)
        self.game.select_number(starting_number)

        # Update game screen display before showing
        game_screen_frame = self.frames.get("game_screen")
        if game_screen_frame:
             game_screen_frame.update_display()

        self.show_frame("game_screen")
        # Note: game_screen.on_show handles triggering AI's first move if needed.

    def record_and_show_result(self):
        """Ends the game, records score (if AI game), and shows the result screen."""
        if not self.game or not self.game.current_state:
            print("Error: Cannot record result, game not initialized.")
            self.show_frame("main_menu")
            return

        # Ensure winner is determined if game ended prematurely
        if self.game.current_state.terminal() and self.game.winner is None:
             self.game.determine_winner()

        winner = self.game.winner if self.game.winner else "Game Incomplete"
        state = self.game.current_state
        # Get final scores correctly mapped to P1/P2
        p1_score = state.pp if state.original_turn == 1 else state.cp
        p2_score = state.cp if state.original_turn == 1 else state.pp

        # --- Score Recording (only for completed AI games) ---
        if self.game.mode == 'AI' and winner != "Game Incomplete":
            game_data = {
                'algorithm': self.game.algorithm,
                'winner': winner,
                'starting_player': self.game.starting_player,
                'initial_number': self.game.initial_number,
                'total_moves': self.game.total_moves,
                'total_ai_time': self.game.total_ai_time, # Include performance stats
                'total_nodes_explored': self.game.total_nodes_explored
            }
            score_manager.add_score(game_data)
        # --- End Score Recording ---

        # Update the result screen UI
        result_screen_frame = self.frames.get("result_screen")
        if result_screen_frame:
             result_screen_frame.set_result(winner, p1_score, p2_score)

        self.show_frame("result_screen") # Navigate to result screen

    def on_closing(self):
        """Handles the window close event."""
        self.destroy() # Close the application

# Application entry point
if __name__ == "__main__":
    app = GameApp()
    app.mainloop() # Start the Tkinter event loop