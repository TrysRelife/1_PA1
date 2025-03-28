import random
import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    """UI Frame for the main menu, allowing game configuration and starting."""

    def __init__(self, controller):
        """Initializes the main menu UI elements and state variables."""
        super().__init__(controller)
        self.controller = controller # Reference to the main app controller
        self.configure(fg_color="#150B3B") # Background color

        # --- State Variables for Game Settings ---
        self.mode_var = ctk.StringVar(value="AI")          # Game mode: 'AI' or '1v1'
        self.algo_var = ctk.StringVar(value="alphabeta")   # AI algorithm: 'minimax' or 'alphabeta'
        self.starting_player_var = ctk.StringVar(value="ai") # Who starts: 'player', 'ai', 'player1', 'player2'
        self.numbers = [] # List to hold generated starting numbers
        self.selected_number_var = ctk.StringVar() # Holds the chosen starting number as a string

        # --- Grid Layout ---
        self.grid_rowconfigure(list(range(8)), weight=0) # Rows have minimal weight
        self.grid_columnconfigure((0, 1, 2), weight=1) # Columns distribute space to center content

        self.create_widgets() # Create all UI elements

        # --- Bindings ---
        # Update UI dynamically when mode changes
        self.mode_var.trace_add("write", self.update_algo_visibility)
        self.mode_var.trace_add("write", self.update_starting_player_options)
        # Set initial UI state based on default variable values
        self.update_algo_visibility()
        self.update_starting_player_options()

    def create_widgets(self):
        """Creates and places all widgets on the main menu frame."""

        # --- Title ---
        self.title_label = ctk.CTkLabel(self, text="Number Division Game", font=("Jura Bold", 32), text_color="white")
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20,10), sticky="ew")

        # --- Game Mode Selection (Radio Buttons) ---
        self.game_mode_label = ctk.CTkLabel(self, text="Game Mode:", font=("Jura", 20), text_color="white")
        self.game_mode_label.grid(row=1, column=0, padx=(20, 5), pady=5, sticky="w")
        self.radio_ai = ctk.CTkRadioButton(self, text="Against AI", variable=self.mode_var, value="AI", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_ai.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.radio_1v1 = ctk.CTkRadioButton(self, text="1v1 (Human vs Human)", variable=self.mode_var, value="1v1", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_1v1.grid(row=1, column=2, padx=(5, 20), pady=5, sticky="w")

        # --- Starting Player Selection (Radio Buttons - created dynamically) ---
        self.starting_player_label = ctk.CTkLabel(self, text="Starting Player:", font=("Jura", 20), text_color="white")
        self.starting_player_label.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="w")
        # Radio buttons themselves are added/updated in `update_starting_player_options`

        # --- AI Algorithm Selection (Radio Buttons - conditionally visible) ---
        self.algo_label = ctk.CTkLabel(self, text="AI Algorithm:", font=("Jura", 20), text_color="white")
        self.algo_label.grid(row=3, column=0, padx=(20, 5), pady=5, sticky="w")
        self.radio_minimax = ctk.CTkRadioButton(self, text="Minimax", variable=self.algo_var, value="minimax", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_minimax.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.radio_alphabeta = ctk.CTkRadioButton(self, text="Alpha-Beta", variable=self.algo_var, value="alphabeta", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_alphabeta.grid(row=3, column=2, padx=(5, 20), pady=5, sticky="w")

        # --- Generate Starting Numbers Button ---
        self.generate_btn = ctk.CTkButton(self, text="Generate Starting Numbers 🎲", command=self.generate_numbers, font=("Jura", 20), width=400, height=40, fg_color="#3E12E7", text_color="white")
        self.generate_btn.grid(row=4, column=0, columnspan=3, pady=10)

        # --- Frame to Hold Number Selection Radio Buttons ---
        self.numbers_frame = ctk.CTkFrame(self, fg_color="transparent") # Transparent frame
        self.numbers_frame.grid(row=5, column=0, columnspan=3, pady=5, sticky="ew")
        self.numbers_frame.grid_columnconfigure(list(range(5)), weight=1) # Configure columns for number buttons

        # --- Start Game Button ---
        self.start_btn = ctk.CTkButton(self, text="Start Game", command=self.start_game, font=("Jura", 22), width=300, height=45, fg_color="#0B8A00", hover_color="#086600", text_color="white", state="disabled") # Disabled until number generated/selected
        self.start_btn.grid(row=6, column=0, columnspan=3, pady=10)

        # --- View High Scores Button ---
        self.highscore_btn = ctk.CTkButton(
            self, text="View High Scores",
            command=lambda: self.controller.show_frame("high_score_screen"), # Navigate to high score screen
            font=("Jura", 20), width=300, height=40,
            fg_color="#E77C12", hover_color="#D6700F", text_color="white"
        )
        self.highscore_btn.grid(row=7, column=0, columnspan=3, pady=(5, 20))

    def update_starting_player_options(self, *args):
        """Updates the 'Starting Player' radio buttons based on the selected game mode (AI vs 1v1)."""
        # Clear existing radio buttons first to avoid duplicates
        if hasattr(self, "starting_player_radio1") and self.starting_player_radio1.winfo_exists():
            self.starting_player_radio1.destroy()
        if hasattr(self, "starting_player_radio2") and self.starting_player_radio2.winfo_exists():
            self.starting_player_radio2.destroy()

        mode = self.mode_var.get()
        # Define button labels and values based on the mode
        if mode == "AI":
            options = [("Player", "player"), ("AI", "ai")]
        else: # '1v1'
            options = [("Player 1", "player1"), ("Player 2", "player2")]

        default_value = options[0][1] # Default selection

        # Create new radio buttons with appropriate text/values
        self.starting_player_radio1 = ctk.CTkRadioButton(self, text=options[0][0], variable=self.starting_player_var, value=options[0][1], font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.starting_player_radio2 = ctk.CTkRadioButton(self, text=options[1][0], variable=self.starting_player_var, value=options[1][1], font=("Jura", 18), fg_color="#3E12E7", text_color="white")

        # Place the new buttons in the grid
        self.starting_player_radio1.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.starting_player_radio2.grid(row=2, column=2, padx=(5, 20), pady=5, sticky="w")

        # Ensure the selected value is valid for the current mode, reset if not
        current_val = self.starting_player_var.get()
        valid_values = [opt[1] for opt in options]
        if current_val not in valid_values:
            self.starting_player_var.set(default_value)

    def update_algo_visibility(self, *args):
        """Shows or hides the AI algorithm selection widgets based on game mode."""
        is_ai_mode = (self.mode_var.get() == "AI")
        # Use grid() to show and grid_remove() to hide, preserving grid configuration
        widgets = [self.algo_label, self.radio_minimax, self.radio_alphabeta]
        for widget in widgets:
            if is_ai_mode:
                widget.grid()
            else:
                widget.grid_remove()

    def generate_valid_numbers(self):
        """Generates a list of up to 5 suitable starting numbers."""
        nums = []

        # Try to find random numbers within a range
        while len(nums) < 5:
            num = random.randint(10000, 20000)

            # Basic check: must be divisible by both 2 and 3 initially
            if num % 2 == 0 and num % 3 == 0:
                     nums.append(num)

        return nums

    def generate_numbers(self):
        """Generates starting numbers and displays them as radio buttons."""
        self.numbers = self.generate_valid_numbers()

        # Clear any previously generated number buttons
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        # Configure grid columns in the numbers_frame based on how many numbers were generated
        num_generated = len(self.numbers)
        for col in range(5): # Max 5 columns
            self.numbers_frame.grid_columnconfigure(col, weight=1 if col < num_generated else 0)

        if self.numbers:
            # Create radio buttons for each generated number
            for idx, num in enumerate(self.numbers):
                btn = ctk.CTkRadioButton(
                    self.numbers_frame,
                    text=f"{num:,}", # Format number with commas
                    variable=self.selected_number_var,
                    value=str(num), # Store value as string
                    font=("Jura", 18), fg_color="#3E12E7", text_color="white",
                )
                # Place button in the next available column
                btn.grid(row=0, column=idx, padx=5, pady=5, sticky="")

            self.selected_number_var.set(str(self.numbers[0])) # Default select the first number
            self.start_btn.configure(state="normal") # Enable the start button
        else:
            # Display a message if no suitable numbers could be generated
            no_num_label = ctk.CTkLabel(self.numbers_frame, text="Could not generate suitable starting numbers.", text_color="yellow")
            no_num_label.grid(row=0, column=0, columnspan=5)
            self.start_btn.configure(state="disabled") # Keep start button disabled

    def start_game(self):
        """Gathers selected settings and tells the main controller to start the game."""
        selected_num_str = self.selected_number_var.get()
        starting_number = int(selected_num_str) # Convert selected number string to int

        # Collect all settings from the UI variables
        settings = {
            'mode': self.mode_var.get(),
            'algorithm': self.algo_var.get(),
            'starting_player': self.starting_player_var.get()
        }
        # Algorithm choice is irrelevant in 1v1 mode
        if settings['mode'] == '1v1':
            settings['algorithm'] = None

        # Pass settings and number to the main app controller to initiate the game
        self.controller.start_new_game(settings, starting_number)

    def on_show(self):
        """Called when the MainMenu frame becomes visible."""
        # Reset state for a fresh menu view
        self.selected_number_var.set("") # Clear number selection
        self.start_btn.configure(state="disabled") # Disable start button
        # Clear any old number radio buttons
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()