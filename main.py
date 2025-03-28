import customtkinter as ctk
import re # For converting class names to keys
from gui.main_menu import MainMenu
from gui.game_screen import GameScreen
from gui.result_screen import ResultScreen
from gui.high_score_screen import HighScoreScreen
from game_logic import Game # Core game logic class
import score_manager # For handling high scores

class GameApp(ctk.CTk):
    """Main application class that manages UI frames and the game instance."""

    def __init__(self):
        """Initializes the main window and creates instances of all UI frames."""
        super().__init__()
        self.title("Number Division Game")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close button

        self.current_frame = None # Holds the currently displayed frame
        self.game = None          # Holds the active Game logic instance

        # Create and store all UI frame instances in a dictionary
        self.frames = {}
        for F in (MainMenu, GameScreen, ResultScreen, HighScoreScreen):
            # Generate a dictionary key from the class name (e.g., MainMenu -> "main_menu")
            name = F.__name__
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            frame_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

            frame = F(controller=self) # Pass the app instance as controller
            self.frames[frame_name] = frame

        self.show_frame("main_menu") # Display the main menu initially

    def show_frame(self, frame_name):
        """Hides the current frame and displays the requested frame."""
        new_frame = self.frames.get(frame_name)

        # Hide the current frame if one exists
        if self.current_frame:
            self.current_frame.pack_forget()

        # Show the new frame
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

        # Call the frame's 'on_show' method if it exists (for frame-specific setup)
        if hasattr(self.current_frame, "on_show"):
            self.current_frame.on_show()

    def start_new_game(self, settings, starting_number):
        """Creates a new Game instance and switches to the game screen."""
        self.game = Game(settings) # Initialize game logic
        self.game.select_number(starting_number) # Set up the initial state

        # Prepare the game screen UI before showing it
        game_screen_frame = self.frames.get("game_screen")
        if game_screen_frame:
             game_screen_frame.update_display() # Ensure UI reflects initial state

        self.show_frame("game_screen")
        # The game_screen's on_show method will handle triggering the AI's first move if needed.

    def record_and_show_result(self):
        """Ends the current game, records scores (if AI mode), and shows the result screen."""

        # Ensure winner is determined, especially if game ended abruptly
        if self.game.current_state.terminal() and self.game.winner is None:
             self.game.determine_winner()

        winner = self.game.winner if self.game.winner else "Game Incomplete"
        state = self.game.current_state
        # Get final scores mapped correctly to P1/P2 regardless of who started
        p1_score = state.pp if state.original_turn == 1 else state.cp
        p2_score = state.cp if state.original_turn == 1 else state.pp

        # --- Record score only for completed AI games ---
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
            score_manager.add_score(game_data) # Add to high scores

        # Update the result screen UI with outcome and scores
        result_screen_frame = self.frames.get("result_screen")
        if result_screen_frame:
             result_screen_frame.set_result(winner, p1_score, p2_score)

        self.show_frame("result_screen") # Navigate to the result screen

    def on_closing(self):
        """Called when the user closes the application window."""
        self.destroy() # Cleanly close the Tkinter application

# --- Application Entry Point ---
if __name__ == "__main__":
    app = GameApp() # Create the application instance
    app.mainloop() # Start the Tkinter event loop