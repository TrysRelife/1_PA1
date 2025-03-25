import random
import customtkinter as ctk
from game_logic import Game

class MainMenu(ctk.CTkFrame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3B")

        # Variables for game settings
        self.mode_var = ctk.StringVar(value="AI")
        self.algo_var = ctk.StringVar(value="alphabeta")
        self.starting_player_var = ctk.StringVar(value="player")
        self.numbers = []
        self.selected_number_var = ctk.StringVar()

        # Configure grid layout (7 rows, 3 columns)
        for r in range(7):
            self.grid_rowconfigure(r, weight=0)
        for c in range(3):
            self.grid_columnconfigure(c, weight=1)

        # Build UI
        self.create_widgets()

        # Bind mode changes to UI updates
        self.mode_var.trace("w", self.update_algo_visibility)
        self.mode_var.trace("w", self.update_starting_player_options)
        self.update_algo_visibility()
        self.update_starting_player_options()

    def create_widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text="Number Division Game",
            font=("Jura Bold", 32),
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        # Game Mode Selection
        self.game_mode_label = ctk.CTkLabel(
            self,
            text="Game Mode:",
            font=("Jura", 20),
            text_color="white"
        )
        self.game_mode_label.grid(row=1, column=0, padx=(20, 5), pady=10, sticky="w")

        self.radio_ai = ctk.CTkRadioButton(
            self,
            text="Against AI",
            variable=self.mode_var,
            value="AI",
            font=("Jura", 18),
            fg_color="#3E12E7",
            text_color="white"
        )
        self.radio_ai.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        self.radio_1v1 = ctk.CTkRadioButton(
            self,
            text="1v1 (Human vs Human)",
            variable=self.mode_var,
            value="1v1",
            font=("Jura", 18),
            fg_color="#3E12E7",
            text_color="white"
        )
        self.radio_1v1.grid(row=1, column=2, padx=(5, 20), pady=10, sticky="w")

        # Starting Player Selection
        self.starting_player_label = ctk.CTkLabel(
            self,
            text="Starting Player:",
            font=("Jura", 20),
            text_color="white"
        )
        self.starting_player_label.grid(row=2, column=0, padx=(20, 5), pady=10, sticky="w")

        # AI Algorithm Selection
        self.algo_label = ctk.CTkLabel(
            self,
            text="AI Algorithm:",
            font=("Jura", 20),
            text_color="white"
        )
        self.algo_label.grid(row=3, column=0, padx=(20, 5), pady=10, sticky="w")

        self.radio_minimax = ctk.CTkRadioButton(
            self,
            text="Minimax",
            variable=self.algo_var,
            value="minimax",
            font=("Jura", 18),
            fg_color="#3E12E7",
            text_color="white"
        )
        self.radio_minimax.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        self.radio_alphabeta = ctk.CTkRadioButton(
            self,
            text="Alpha-Beta",
            variable=self.algo_var,
            value="alphabeta",
            font=("Jura", 18),
            fg_color="#3E12E7",
            text_color="white"
        )
        self.radio_alphabeta.grid(row=3, column=2, padx=(5, 20), pady=10, sticky="w")

        # Generate Numbers Button
        self.generate_btn = ctk.CTkButton(
            self,
            text="Generate Starting Numbers 🎲",
            command=self.generate_numbers,
            font=("Jura", 20),
            width=400,
            height=45,
            fg_color="#3E12E7",
            text_color="white"
        )
        self.generate_btn.grid(row=4, column=0, columnspan=3, pady=5)

        # Numbers Frame
        self.numbers_frame = ctk.CTkFrame(self, fg_color="#150B3B")
        self.numbers_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")
        self.numbers_frame.grid_columnconfigure(0, weight=1)

        # Start Game Button
        self.start_btn = ctk.CTkButton(
            self,
            text="Start Game",
            command=self.start_game,
            font=("Jura", 22),
            width=300,
            height=50,
            fg_color="#3E12E7",
            text_color="white",
            state="disabled"
        )
        self.start_btn.grid(row=6, column=0, columnspan=3, pady=(5, 10))

    def update_starting_player_options(self, *args):
        # Update starting player options based on game mode
        if hasattr(self, "starting_player_radio1"):
            self.starting_player_radio1.destroy()
        if hasattr(self, "starting_player_radio2"):
            self.starting_player_radio2.destroy()

        options = [("Player", "player"), ("AI", "ai")] if self.mode_var.get() == "AI" else [("Player 1", "player1"), ("Player 2", "player2")]

        self.starting_player_radio1 = ctk.CTkRadioButton(
            self,
            text=options[0][0],
            variable=self.starting_player_var,
            value=options[0][1],
            font=("Jura", 18),
            fg_color="#3E12E7",
            text_color="white"
        )
        self.starting_player_radio2 = ctk.CTkRadioButton(
            self,
            text=options[1][0],
            variable=self.starting_player_var,
            value=options[1][1],
            font=("Jura", 18),
            fg_color="#3E12E7",
            text_color="white"
        )

        self.starting_player_radio1.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        self.starting_player_radio2.grid(row=2, column=2, padx=(5, 20), pady=10, sticky="w")
        self.starting_player_var.set(options[0][1])
        self.starting_player_var.set("ai")

    def update_algo_visibility(self, *args):
        # Show/hide AI algorithm options based on game mode
        if self.mode_var.get() == "AI":
            self.algo_label.grid()
            self.radio_minimax.grid()
            self.radio_alphabeta.grid()
        else:
            self.algo_label.grid_remove()
            self.radio_minimax.grid_remove()
            self.radio_alphabeta.grid_remove()

    def generate_valid_numbers(self):
        # Generate 5 valid starting numbers
        nums = []
        while len(nums) < 5:
            num = random.randint(10000, 20000)
            if num % 2 == 0 and num % 3 == 0:
                nums.append(num)
        return nums

    def generate_numbers(self):
        # Display generated numbers as radio buttons
        self.numbers = self.generate_valid_numbers()
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        for col in range(len(self.numbers)):
            self.numbers_frame.grid_columnconfigure(col, weight=1)

        for idx, num in enumerate(self.numbers):
            btn = ctk.CTkRadioButton(
                self.numbers_frame,
                text=str(num),
                variable=self.selected_number_var,
                value=str(num),
                font=("Jura", 20),
                fg_color="#3E12E7",
                text_color="white",
                width=100,
                height=40
            )
            btn.grid(row=0, column=idx, padx=10, pady=5, sticky="")

        if self.numbers:
            self.selected_number_var.set(str(self.numbers[0]))
            self.start_btn.configure(state="normal")

    def start_game(self):
        # Start game with selected settings
        if not self.selected_number_var.get():
            return

        settings = {
            'algorithm': self.algo_var.get(),
            'mode': self.mode_var.get(),
            'starting_player': self.starting_player_var.get()
        }
        starting_number = int(self.selected_number_var.get())
        self.controller.start_new_game(settings, starting_number)

    def on_show(self):
        # Reset menu when shown
        self.selected_number_var.set("")
        self.start_btn.configure(state="disabled")
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()