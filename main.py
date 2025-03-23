import customtkinter as ctk
from gui.main_menu import MainMenu
from gui.game_screen import GameScreen
from gui.result_screen import ResultScreen
from game_logic import Game

class GameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Number Division Game")  # Set window title
        self.geometry("800x600")  # Set window size
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

        self.current_frame = None  # Track the currently displayed frame
        self.game = None  # Store the current game instance

        # Create all frames (screens) for the application
        frame_classes = [
            ("main_menu", MainMenu),
            ("game_screen", GameScreen),
            ("result_screen", ResultScreen)
        ]
        self.frames = {name: cls(self) for name, cls in frame_classes}  # Initialize frames

        self.show_frame("main_menu")  # Start with the main menu

    def show_frame(self, frame_name):
        # Switch to the specified frame
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide the current frame
        self.current_frame = self.frames[frame_name]  # Set the new frame
        self.current_frame.pack(fill="both", expand=True)  # Display the new frame

        # Call the frame's on_show method if it exists
        if hasattr(self.current_frame, "on_show"):
            self.current_frame.on_show()

    def start_new_game(self, settings, starting_number):
        # Initialize a new game with the provided settings and starting number
        self.game = Game(settings)
        self.game.select_number(starting_number)  # Set the starting number
        self.frames["game_screen"].update_display()  # Update the game screen display
        self.show_frame("game_screen")  # Switch to the game screen

        # If it's the AI's turn, trigger the AI move
        if self.game.mode == 'AI' and self.game.turn == 2:
            self.frames["game_screen"].on_show()
            self.frames["game_screen"].computer_turn()

    def show_result(self, result, player1_score=None, player2_score=None):
        # Display the result screen with the game outcome
        self.frames["result_screen"].set_result(result, player1_score, player2_score)
        self.show_frame("result_screen")

    def on_closing(self):
        # Handle window closing event
        self.destroy()  # Close the application

if __name__ == "__main__":
    app = GameApp()  # Create the application instance
    app.mainloop()  # Start the main event loop