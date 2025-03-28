import customtkinter as ctk
import score_manager # To load high score data

class HighScoreScreen(ctk.CTkFrame):
    """UI Frame for displaying high scores recorded from games against the AI."""

    def __init__(self, controller):
        """Initializes the high score screen UI elements."""
        super().__init__(controller)
        self.controller = controller # Reference to the main app controller
        self.configure(fg_color="#150B3B") # Background color

        # Configure grid layout for responsive design
        self.grid_columnconfigure(0, weight=1) # Center content horizontally
        self.grid_rowconfigure(0, weight=0) # Title row
        self.grid_rowconfigure(1, weight=0) # Button row
        self.grid_rowconfigure(2, weight=1) # Score display textbox (expandable)
        self.grid_rowconfigure(3, weight=0) # Back button row

        # --- UI Elements ---
        self.title_label = ctk.CTkLabel(self, text="High Scores (vs AI)", font=("Jura Bold", 28), text_color="white")
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        # Frame to hold algorithm selection buttons horizontally
        self.algo_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.algo_button_frame.grid(row=1, column=0, pady=5)

        # Button to show Alpha-Beta scores
        self.btn_show_alphabeta = ctk.CTkButton(
            self.algo_button_frame, text="Alpha-Beta Scores",
            command=lambda: self.load_and_display_scores('alphabeta'),
            font=("Jura", 16), fg_color="#3E12E7"
        )
        self.btn_show_alphabeta.pack(side="left", padx=10)

        # Button to show Minimax scores
        self.btn_show_minimax = ctk.CTkButton(
            self.algo_button_frame, text="Minimax Scores",
            command=lambda: self.load_and_display_scores('minimax'),
            font=("Jura", 16), fg_color="#E77C12"
        )
        self.btn_show_minimax.pack(side="left", padx=10)

        # Textbox for displaying the formatted scores
        self.score_display = ctk.CTkTextbox(
            self, font=("Consolas", 12), # Monospaced font for better alignment
            wrap="none", fg_color="#2A1B5C", text_color="white",
            border_width=1, border_color="#3E12E7"
        )
        self.score_display.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 10))
        self.score_display.configure(state="disabled") # Make it read-only

        # Button to navigate back to the main menu
        self.btn_back = ctk.CTkButton(
            self, text="Back to Menu",
            command=lambda: self.controller.show_frame("main_menu"),
            font=("Jura", 18), width=200, height=40, fg_color="#5C1500"
        )
        self.btn_back.grid(row=3, column=0, pady=(10, 20))

    def format_scores(self, score_list):
        """Formats a list of score dictionaries into a neatly aligned string."""
        if not score_list:
            return "No scores recorded yet for this algorithm."

        # Define headers and separator for the table-like format
        header = (f"{'#':<3}{'Winner':<10}{'Start Player':<14}{'Initial N':<12}"
                  f"{'Moves':<7}{'AI Time (s)':<38}{'Nodes Explored':<17}\n")
        separator = "-" * 101 + "\n" # Adjust length based on header
        lines = [header, separator]

        # Format each score entry, showing newest first
        for i, score in enumerate(reversed(score_list), 1): # Use reversed for newest first
             lines.append(
                 f"{i:<3}" # Index
                 f"{score.get('winner', 'N/A'):<10}"
                 f"{score.get('starting_player', 'N/A').capitalize():<14}"
                 f"{score.get('initial_number', 0):<12,}" # Number with comma separator
                 f"{score.get('total_moves', 0):<7}"
                 f"{score.get('total_ai_time', 0.0):<38,.30f}" # AI time with high precision
                 f"{score.get('total_nodes_explored', 0):<17,}" # Nodes with comma separator
                 "\n"
             )
        return "".join(lines) # Combine all lines into a single string

    def load_and_display_scores(self, algorithm):
        """Loads scores for the specified algorithm and updates the display."""
        all_scores = score_manager.load_scores() # Get all scores from file
        scores_to_display = all_scores.get(algorithm, []) # Get list for the chosen algorithm
        formatted_text = self.format_scores(scores_to_display) # Format the list

        # Update the textbox content
        self.score_display.configure(state="normal") # Enable writing temporarily
        self.score_display.delete("1.0", "end")      # Clear existing content
        self.score_display.insert("1.0", formatted_text) # Insert new formatted text
        self.score_display.configure(state="disabled") # Make read-only again

    def on_show(self):
        """Called when this frame becomes visible. Loads default scores."""
        # Default to showing Alpha-Beta scores when the screen is first opened
        self.load_and_display_scores('alphabeta')