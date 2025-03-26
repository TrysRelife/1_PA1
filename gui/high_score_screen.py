import customtkinter as ctk
import score_manager # Handles score loading/saving

class HighScoreScreen(ctk.CTkFrame):
    """
    Displays high scores, allowing filtering by AI algorithm.
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3B")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=0) # Buttons
        self.grid_rowconfigure(2, weight=1) # Textbox (expandable)
        self.grid_rowconfigure(3, weight=0) # Back button

        # --- UI Elements ---
        self.title_label = ctk.CTkLabel(self, text="High Scores (vs AI)", font=("Jura Bold", 28), text_color="white")
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        # Frame for algorithm selection buttons
        self.algo_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.algo_button_frame.grid(row=1, column=0, pady=5)

        self.btn_show_alphabeta = ctk.CTkButton(
            self.algo_button_frame, text="Alpha-Beta Scores",
            command=lambda: self.load_and_display_scores('alphabeta'),
            font=("Jura", 16), fg_color="#3E12E7"
        )
        self.btn_show_alphabeta.pack(side="left", padx=10)

        self.btn_show_minimax = ctk.CTkButton(
            self.algo_button_frame, text="Minimax Scores",
            command=lambda: self.load_and_display_scores('minimax'),
            font=("Jura", 16), fg_color="#E77C12"
        )
        self.btn_show_minimax.pack(side="left", padx=10)

        # Textbox for displaying scores
        self.score_display = ctk.CTkTextbox(
            self, font=("Consolas", 12), # Monospaced font for alignment
            wrap="none", fg_color="#2A1B5C", text_color="white",
            border_width=1, border_color="#3E12E7"
        )
        self.score_display.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 10))
        self.score_display.configure(state="disabled") # Read-only

        # Back button
        self.btn_back = ctk.CTkButton(
            self, text="Back to Menu",
            command=lambda: self.controller.show_frame("main_menu"),
            font=("Jura", 18), width=200, height=40, fg_color="#5C1500"
        )
        self.btn_back.grid(row=3, column=0, pady=(10, 20))

    def format_scores(self, score_list):
        """Formats a list of score dictionaries into a string for display with aligned columns."""
        if not score_list:
            return "No scores recorded yet for this algorithm."

        # Define headers and column widths for alignment
        header = (f"{'#':<3}{'Winner':<10}{'Start Player':<14}{'Initial N':<12}"
                  f"{'Moves':<7}{'AI Time (s)':<38}{'Nodes Explored':<17}\n")
        separator = "-" * 101 + "\n"
        lines = [header, separator]

        # Format each score entry (newest first)
        for i, score in enumerate(reversed(score_list), 1):
             lines.append(
                 f"{i:<3}"
                 f"{score.get('winner', 'N/A'):<10}"
                 f"{score.get('starting_player', 'N/A').capitalize():<14}"
                 f"{score.get('initial_number', 0):<12,}"
                 f"{score.get('total_moves', 0):<7}"
                 f"{score.get('total_ai_time', 0.0):<38,.30f}" # High precision time
                 f"{score.get('total_nodes_explored', 0):<17,}"
                 "\n"
             )
        return "".join(lines)

    def load_and_display_scores(self, algorithm):
        """Loads scores for the specified algorithm and updates the textbox."""
        all_scores = score_manager.load_scores()
        scores_to_display = all_scores.get(algorithm, [])
        formatted_text = self.format_scores(scores_to_display)

        # Update textbox content
        self.score_display.configure(state="normal") # Enable writing
        self.score_display.delete("1.0", "end")
        self.score_display.insert("1.0", formatted_text)
        self.score_display.configure(state="disabled") # Disable writing

    def on_show(self):
        """Called when the HighScoreScreen becomes visible. Loads default scores."""
        # Default to showing Alpha-Beta scores
        self.load_and_display_scores('alphabeta')