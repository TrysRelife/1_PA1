import customtkinter as ctk

class ResultScreen(ctk.CTkFrame):
    """
    Displays the game outcome (Winner/Loser/Draw) and final scores.
    Provides a button to return to the main menu.
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3B")

        # Configure grid to center content
        self.grid_rowconfigure((0, 2), weight=1) # Spacers
        self.grid_rowconfigure(1, weight=0) # Content
        self.grid_columnconfigure(0, weight=1) # Center horizontally

        # Central frame for content
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=1, column=0, sticky="")

        # Result label (text set later)
        self.result_label = ctk.CTkLabel(
            self.center_frame, text="", font=("Jura Bold", 30),
            fg_color="transparent", text_color="white", justify="center"
        )
        self.result_label.pack(pady=(0, 30))

        # Main menu button
        self.btn_main_menu = ctk.CTkButton(
            self.center_frame, text="Main Menu",
            command=lambda: self.controller.show_frame("main_menu"),
            fg_color="#3D11E6", hover_color="#300DBA", text_color="white",
            font=("Jura", 18), width=180, height=40
        )
        self.btn_main_menu.pack(pady=20)

    def set_result(self, winner_text, player1_score=None, player2_score=None):
        """Updates the result label with the game outcome and scores."""
        result_display_text = f"{winner_text}\n\n"

        if player1_score is not None and player2_score is not None:
            # Determine labels based on game mode ('Player'/'AI' or 'Player 1'/'Player 2')
            p1_label = "Player 1"
            p2_label = "Player 2"
            if hasattr(self.controller, 'game') and self.controller.game and self.controller.game.mode == 'AI':
                 p1_label = "Player"
                 p2_label = "AI"

            result_display_text += f"{p1_label}: {player1_score}\n{p2_label}: {player2_score}"

        self.result_label.configure(text=result_display_text)

    def on_show(self):
        """Called automatically when the ResultScreen becomes visible."""
        pass # No actions needed on show