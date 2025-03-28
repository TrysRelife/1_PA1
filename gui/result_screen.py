import customtkinter as ctk

class ResultScreen(ctk.CTkFrame):
    """UI Frame for displaying the game's outcome (winner/draw) and final scores."""

    def __init__(self, controller):
        """Initializes the result screen UI elements."""
        super().__init__(controller)
        self.controller = controller # Reference to the main app controller
        self.configure(fg_color="#150B3B") # Background color

        # Configure grid to center the content vertically and horizontally
        self.grid_rowconfigure((0, 2), weight=1) # Add empty space above and below content
        self.grid_rowconfigure(1, weight=0)      # Content row takes minimal space
        self.grid_columnconfigure(0, weight=1)   # Center content horizontally

        # Central frame to hold the result label and button
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=1, column=0, sticky="") # Place in the middle cell

        # Label to display winner/draw message and scores (text set dynamically)
        self.result_label = ctk.CTkLabel(
            self.center_frame, text="", font=("Jura Bold", 30),
            fg_color="transparent", text_color="white", justify="center" # Center-align multi-line text
        )
        self.result_label.pack(pady=(0, 30)) # Add padding below the label

        # Button to return to the main menu
        self.btn_main_menu = ctk.CTkButton(
            self.center_frame, text="Main Menu",
            command=lambda: self.controller.show_frame("main_menu"), # Navigate back
            fg_color="#3D11E6", hover_color="#300DBA", text_color="white",
            font=("Jura", 18), width=180, height=40
        )
        self.btn_main_menu.pack(pady=20) # Add padding around the button

    def set_result(self, winner_text, player1_score=None, player2_score=None):
        """Updates the result label with the outcome and final scores."""
        # Start with the winner message (e.g., "Player Wins!", "AI Wins!", "Draw")
        result_display_text = f"{winner_text}\n\n" # Add newlines for spacing

        # Append scores if provided
        if self.controller.game.mode == 'AI':
                 # Need the original_turn from the game state
                 # Ensure game and state exist before accessing
                 original_turn = 1 # Default assumption (if somehow state is missing)
                 if self.controller.game.current_state:
                      original_turn = self.controller.game.current_state.original_turn

                 if original_turn == 1: # Player is P1, AI is P2
                     player_final_score = player1_score
                     ai_final_score = player2_score
                 else: # AI is P1, Player is P2
                     player_final_score = player2_score
                     ai_final_score = player1_score
                 result_display_text += f"Player: {player_final_score}\nAI: {ai_final_score}"
        else: # 1v1 Mode or fallback
                result_display_text += f"Player 1: {player1_score}\nPlayer 2: {player2_score}"
            

        # Configure the label widget with the combined text
        self.result_label.configure(text=result_display_text)

    def on_show(self):
        """Called automatically when the ResultScreen frame becomes visible."""
        pass