import random
import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    """
    Represents the main menu screen for game setup.
    Allows selecting mode, AI algorithm, starting player, and starting number.
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3B")

        # --- State Variables for Game Settings ---
        self.mode_var = ctk.StringVar(value="AI") # 'AI' or '1v1'
        self.algo_var = ctk.StringVar(value="alphabeta") # 'minimax' or 'alphabeta'
        self.starting_player_var = ctk.StringVar(value="player") # 'player', 'ai', 'player1', 'player2'
        self.numbers = [] # List to hold generated starting numbers
        self.selected_number_var = ctk.StringVar() # Holds the chosen number string

        # --- Grid Layout Configuration ---
        for r in range(8):
            self.grid_rowconfigure(r, weight=0)
        self.grid_columnconfigure((0, 1, 2), weight=1) # Center content

        self.create_widgets()

        # Bind UI updates to variable changes
        self.mode_var.trace_add("write", self.update_algo_visibility)
        self.mode_var.trace_add("write", self.update_starting_player_options)
        # Initialize UI state based on defaults
        self.update_algo_visibility()
        self.update_starting_player_options()

    def create_widgets(self):
        """Creates and arranges all UI elements on the main menu."""

        # --- Title ---
        self.title_label = ctk.CTkLabel(self, text="Number Division Game", font=("Jura Bold", 32), text_color="white")
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20,10), sticky="ew")

        # --- Game Mode Selection ---
        self.game_mode_label = ctk.CTkLabel(self, text="Game Mode:", font=("Jura", 20), text_color="white")
        self.game_mode_label.grid(row=1, column=0, padx=(20, 5), pady=5, sticky="w")
        self.radio_ai = ctk.CTkRadioButton(self, text="Against AI", variable=self.mode_var, value="AI", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_ai.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.radio_1v1 = ctk.CTkRadioButton(self, text="1v1 (Human vs Human)", variable=self.mode_var, value="1v1", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_1v1.grid(row=1, column=2, padx=(5, 20), pady=5, sticky="w")

        # --- Starting Player Selection ---
        self.starting_player_label = ctk.CTkLabel(self, text="Starting Player:", font=("Jura", 20), text_color="white")
        self.starting_player_label.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="w")
        # (Radio buttons created/updated dynamically)

        # --- AI Algorithm Selection (Visible only in AI mode) ---
        self.algo_label = ctk.CTkLabel(self, text="AI Algorithm:", font=("Jura", 20), text_color="white")
        self.algo_label.grid(row=3, column=0, padx=(20, 5), pady=5, sticky="w")
        self.radio_minimax = ctk.CTkRadioButton(self, text="Minimax", variable=self.algo_var, value="minimax", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_minimax.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.radio_alphabeta = ctk.CTkRadioButton(self, text="Alpha-Beta", variable=self.algo_var, value="alphabeta", font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.radio_alphabeta.grid(row=3, column=2, padx=(5, 20), pady=5, sticky="w")

        # --- Generate Starting Numbers ---
        self.generate_btn = ctk.CTkButton(self, text="Generate Starting Numbers 🎲", command=self.generate_numbers, font=("Jura", 20), width=400, height=40, fg_color="#3E12E7", text_color="white")
        self.generate_btn.grid(row=4, column=0, columnspan=3, pady=10)

        # --- Frame to Hold Number Selection Radio Buttons ---
        self.numbers_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.numbers_frame.grid(row=5, column=0, columnspan=3, pady=5, sticky="ew")
        self.numbers_frame.grid_columnconfigure(list(range(5)), weight=1) # Allow up to 5 numbers

        # --- Start Game Button ---
        self.start_btn = ctk.CTkButton(self, text="Start Game", command=self.start_game, font=("Jura", 22), width=300, height=45, fg_color="#0B8A00", hover_color="#086600", text_color="white", state="disabled") # Disabled initially
        self.start_btn.grid(row=6, column=0, columnspan=3, pady=10)

        # --- View High Scores Button ---
        self.highscore_btn = ctk.CTkButton(
            self, text="View High Scores",
            command=lambda: self.controller.show_frame("high_score_screen"),
            font=("Jura", 20), width=300, height=40,
            fg_color="#E77C12", hover_color="#D6700F", text_color="white"
        )
        self.highscore_btn.grid(row=7, column=0, columnspan=3, pady=(5, 20))

    def update_starting_player_options(self, *args):
        """Updates the 'Starting Player' radio buttons based on the selected game mode."""
        # Destroy existing buttons
        if hasattr(self, "starting_player_radio1") and self.starting_player_radio1.winfo_exists():
            self.starting_player_radio1.destroy()
        if hasattr(self, "starting_player_radio2") and self.starting_player_radio2.winfo_exists():
            self.starting_player_radio2.destroy()

        mode = self.mode_var.get()
        # Define text/values based on mode
        if mode == "AI":
            options = [("Player", "player"), ("AI", "ai")]
        else: # '1v1'
            options = [("Player 1", "player1"), ("Player 2", "player2")]

        default_value = options[0][1]

        # Create new radio buttons
        self.starting_player_radio1 = ctk.CTkRadioButton(self, text=options[0][0], variable=self.starting_player_var, value=options[0][1], font=("Jura", 18), fg_color="#3E12E7", text_color="white")
        self.starting_player_radio2 = ctk.CTkRadioButton(self, text=options[1][0], variable=self.starting_player_var, value=options[1][1], font=("Jura", 18), fg_color="#3E12E7", text_color="white")

        # Place new buttons
        self.starting_player_radio1.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.starting_player_radio2.grid(row=2, column=2, padx=(5, 20), pady=5, sticky="w")

        # Reset selection if current value is invalid for the new mode
        current_val = self.starting_player_var.get()
        valid_values = [opt[1] for opt in options]
        if current_val not in valid_values:
            self.starting_player_var.set(default_value)

    def update_algo_visibility(self, *args):
        """Shows or hides the AI algorithm selection widgets based on the game mode."""
        if self.mode_var.get() == "AI":
            self.algo_label.grid()
            self.radio_minimax.grid()
            self.radio_alphabeta.grid()
        else: # Hide for 1v1
            self.algo_label.grid_remove()
            self.radio_minimax.grid_remove()
            self.radio_alphabeta.grid_remove()

    def generate_valid_numbers(self):
        """Generates a list of up to 5 valid starting numbers (divisible by 2/3, allow moves)."""
        nums = []
        attempts = 0
        min_steps_needed = 2 # Require numbers allowing at least 2 divisions

        while len(nums) < 5 and attempts < 1000:
            attempts += 1
            num = random.randint(10000, 50000)

            # Check if number allows initial moves and a few subsequent ones
            if num % 2 == 0 and num % 3 == 0:
                 temp_n = num
                 steps = 0
                 while temp_n > 1 and (temp_n % 2 == 0 or temp_n % 3 == 0) and steps < min_steps_needed + 1:
                     if temp_n % 3 == 0: temp_n //= 3
                     elif temp_n % 2 == 0: temp_n //= 2
                     steps += 1

                 if steps >= min_steps_needed and num not in nums:
                     nums.append(num)

        # Add backups if needed
        if len(nums) < 5:
            backup_nums = [12600, 15120, 18900, 25200, 30240, 37800, 43200]
            for bn in backup_nums:
                if len(nums) >= 5: break
                if bn not in nums:
                    nums.append(bn)

        return sorted(nums[:5]) # Return up to 5 numbers, sorted

    def generate_numbers(self):
        """Generates numbers and displays them as radio buttons, enables start button."""
        self.numbers = self.generate_valid_numbers()

        # Clear previous number buttons
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        # Configure grid columns based on how many numbers were generated
        num_generated = len(self.numbers)
        for col in range(5):
            self.numbers_frame.grid_columnconfigure(col, weight=1 if col < num_generated else 0)

        if self.numbers:
            # Create radio buttons for each number
            for idx, num in enumerate(self.numbers):
                btn = ctk.CTkRadioButton(
                    self.numbers_frame, text=f"{num:,}", variable=self.selected_number_var,
                    value=str(num), font=("Jura", 18), fg_color="#3E12E7", text_color="white",
                )
                btn.grid(row=0, column=idx, padx=5, pady=5, sticky="")

            self.selected_number_var.set(str(self.numbers[0])) # Select first number
            self.start_btn.configure(state="normal") # Enable start
        else:
            # Show message if no numbers generated
            no_num_label = ctk.CTkLabel(self.numbers_frame, text="Could not generate suitable starting numbers.", text_color="yellow")
            no_num_label.grid(row=0, column=0, columnspan=5)
            self.start_btn.configure(state="disabled") # Keep start disabled

    def start_game(self):
        """Collects settings and chosen number, then tells the controller to start."""
        selected_num_str = self.selected_number_var.get()
        if not selected_num_str:
            print("Error: No starting number selected.")
            return

        try:
            starting_number = int(selected_num_str)
        except ValueError:
            print(f"Error: Invalid starting number format: {selected_num_str}")
            return

        settings = {
            'mode': self.mode_var.get(),
            'algorithm': self.algo_var.get(),
            'starting_player': self.starting_player_var.get()
        }
        # Algorithm is irrelevant in 1v1 mode
        if settings['mode'] == '1v1':
            settings['algorithm'] = None

        self.controller.start_new_game(settings, starting_number)

    def on_show(self):
        """Called when the MainMenu becomes visible. Resets number selection."""
        self.selected_number_var.set("")
        self.start_btn.configure(state="disabled")
        # Clear number radio buttons
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()