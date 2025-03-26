import customtkinter as ctk
import random # Used for the number shaking animation

class GameScreen(ctk.CTkFrame):
    """
    Represents the game screen, displaying the current number, scores, bank,
    turn indicator, and action buttons. Handles user input and AI turns.
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3C")
        self.create_widgets()
        self.bind("<Configure>", self.on_resize) # Adjust font sizes dynamically
        self._after_id = None # For pending 'after' calls (e.g., AI delay)

        # Variables for the shaking animation
        self.shake_offset = 5
        self.shake_delay = 50
        self.shake_count = 0
        self.max_shakes = 6

    def create_widgets(self):
        """Creates and arranges all the UI elements within the frame."""

        # --- Top Frame for Scores and Turn ---
        self.top_frame = ctk.CTkFrame(self, fg_color="#150B3C", height=60)
        self.top_frame.place(relx=0.5, rely=0.0, anchor="n", relwidth=1.0)

        self.score_label_1 = ctk.CTkLabel(self.top_frame, text="Player: 0", font=("Jura", 12),
                                         fg_color="transparent", text_color="white")
        self.score_label_1.place(relx=0.02, rely=0.5, anchor="w")

        self.score_label_2 = ctk.CTkLabel(self.top_frame, text="AI: 0", font=("Jura", 12),
                                         fg_color="transparent", text_color="white")
        self.score_label_2.place(relx=0.98, rely=0.5, anchor="e")

        self.turn_label = ctk.CTkLabel(self.top_frame, text="YOUR TURN", font=("Jura Bold", 28),
                                      fg_color="transparent", text_color="white")
        self.turn_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Main Game Area ---
        self.current_number_label = ctk.CTkLabel(self, text="0", font=("Jura Bold", 100),
                                                fg_color="transparent", text_color="white")
        self.current_number_label.place(relx=0.5, rely=0.4, anchor="center")

        self.bank_label = ctk.CTkLabel(self, text="Bank: 0", font=("Jura Bold", 32),
                                      fg_color="transparent", text_color="white")
        self.bank_label.place(relx=0.5, rely=0.55, anchor="center")

        self.last_move_label = ctk.CTkLabel(self, text="Last move: -", font=("Jura", 12),
                                          fg_color="transparent", text_color="white")
        self.last_move_label.place(relx=0.02, rely=0.3, anchor="w")

        # --- Action Buttons ---
        self.btn_divide2 = ctk.CTkButton(self, text="÷ 2", command=lambda: self.handle_move(2),
                                         fg_color="#E77C12", text_color="white", font=("Jura", 22),
                                         width=150, height=60, corner_radius=10, hover_color="#D6700F")
        self.btn_divide2.place(relx=0.35, rely=0.7, anchor="center")

        self.btn_divide3 = ctk.CTkButton(self, text="÷ 3", command=lambda: self.handle_move(3),
                                         fg_color="#3E12E7", text_color="white", font=("Jura", 22),
                                         width=150, height=60, corner_radius=10, hover_color="#360FC4")
        self.btn_divide3.place(relx=0.65, rely=0.7, anchor="center")

        self.btn_end_game = ctk.CTkButton(self, text="End Game / Show Result", command=self.end_game,
                                        fg_color="#5C1500", text_color="white", font=("Jura", 20),
                                        width=250, height=50, hover_color="#4A1000")
        self.btn_end_game.place(relx=0.5, rely=0.85, anchor="center")

    def on_resize(self, event):
        """Adjusts font sizes dynamically when the window size changes."""
        width = self.winfo_width()
        height = self.winfo_height()
        if width < 100 or height < 100: return # Avoid calculations for tiny sizes during init

        # Calculate font sizes based on window dimensions with min/max limits
        base_width = 800
        scale_factor = width / base_width
        current_font_size = max(30, min(120, int(height * 0.15)))
        turn_bank_font_size = max(18, min(40, int(scale_factor * 32)))
        scores_font_size = max(10, min(20, int(scale_factor * 14)))
        button_font_size = max(14, min(26, int(scale_factor * 22)))
        end_button_font_size = max(14, min(22, int(scale_factor * 20)))

        # Apply the calculated font sizes
        self.current_number_label.configure(font=("Jura Bold", current_font_size))
        self.turn_label.configure(font=("Jura Bold", turn_bank_font_size))
        self.bank_label.configure(font=("Jura Bold", turn_bank_font_size))
        self.score_label_1.configure(font=("Jura", scores_font_size))
        self.score_label_2.configure(font=("Jura", scores_font_size))
        self.last_move_label.configure(font=("Jura", scores_font_size))
        self.btn_divide2.configure(font=("Jura", button_font_size))
        self.btn_divide3.configure(font=("Jura", button_font_size))
        self.btn_end_game.configure(font=("Jura", end_button_font_size))

    def handle_move(self, divisor):
        """Processes a player's move, updates state/UI, and triggers AI if needed."""
        if self.controller.game.current_state.terminal():
            return # Ignore moves if game over

        self.controller.game.make_move(divisor)
        self.last_move_label.configure(text=f"Last move: / {divisor}")
        self.update_display()
        self.start_shaking_number() # Visual feedback

        if self.controller.game.current_state.terminal():
            self.update_buttons()
            self.after(500, self.end_game) # Show results after short delay
            return

        self.update_buttons()

        # If playing against AI and it's AI's turn now
        if self.controller.game.mode == 'AI' and self.controller.game.turn == 2:
            self.computer_turn()

    def computer_turn(self):
        """Initiates the AI's turn with a thinking delay."""
        self.turn_label.configure(text="AI THINKING...")
        self.btn_divide2.configure(state="disabled")
        self.btn_divide3.configure(state="disabled")

        if self._after_id:
            self.after_cancel(self._after_id)

        # Schedule the actual AI move calculation after 1 second
        self._after_id = self.after(1000, self.perform_computer_move)

    def perform_computer_move(self):
        """Executes the AI's move calculation and updates the UI."""
        self._after_id = None

        if self.controller.game.current_state.terminal():
             self.end_game()
             return

        divisor = self.controller.game.computer_move() # Get AI move from logic

        if divisor is not None:
            self.last_move_label.configure(text=f"Last move: / {divisor}")
            self.update_display()
            self.start_shaking_number()

            if self.controller.game.current_state.terminal():
                self.update_buttons()
                self.after(500, self.end_game)
            else:
                self.update_buttons() # Re-enable player buttons for their turn
        else:
            # Fallback if AI fails to move (should be rare)
            print("AI had no move, ending game.")
            if not self.controller.game.current_state.terminal():
                 self.controller.game.determine_winner()
            self.update_buttons()
            self.end_game()

    def update_display(self):
        """Refreshes all UI elements based on the current game state."""
        state = self.controller.game.get_game_state()
        if not state: return

        current_number = state.n
        self.current_number_label.configure(text=f"{current_number:,}" if current_number > 0 else "0")
        self.bank_label.configure(text=f"Bank: {state.b}")

        # Map internal scores (pp, cp) to P1/P2 based on who started
        p1_score = state.pp if state.original_turn == 1 else state.cp
        p2_score = state.cp if state.original_turn == 1 else state.pp

        # Update labels based on game mode
        if self.controller.game.mode == '1v1':
            self.score_label_1.configure(text=f"PLAYER 1: {p1_score}")
            self.score_label_2.configure(text=f"PLAYER 2: {p2_score}")
            player_turn_text = '1' if self.controller.game.turn == 1 else '2'
            turn_text = f"PLAYER {player_turn_text}'S TURN" if not state.terminal() else "GAME OVER"
        else: # AI Mode
            self.score_label_1.configure(text=f"PLAYER: {p1_score}")
            self.score_label_2.configure(text=f"AI: {p2_score}")
            turn_text = "YOUR TURN" if self.controller.game.turn == 1 else "AI TURN"
            if state.terminal():
                 turn_text = "GAME OVER"
            elif self.controller.game.turn == 2 and self._after_id: # Show thinking state
                turn_text = "AI THINKING..."

        self.turn_label.configure(text=turn_text)

    def update_buttons(self):
        """Enables/disables division buttons based on divisibility and current turn."""
        state = self.controller.game.get_game_state()
        if not state or state.terminal():
            self.btn_divide2.configure(state="disabled")
            self.btn_divide3.configure(state="disabled")
            return

        current_number = state.n
        # Player buttons active only if it's their turn (always in 1v1, only turn 1 in AI)
        is_player_turn = True
        if self.controller.game.mode == 'AI' and self.controller.game.turn == 2:
            is_player_turn = False

        self.btn_divide2.configure(state="normal" if current_number % 2 == 0 and is_player_turn else "disabled")
        self.btn_divide3.configure(state="normal" if current_number % 3 == 0 and is_player_turn else "disabled")

    def end_game(self):
        """Stops pending actions and transitions to the result screen."""
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        self.last_move_label.configure(text="Last move: -") # Reset for next game
        self.controller.record_and_show_result()

    def on_show(self):
        """Called when the GameScreen becomes visible. Sets initial state."""
        if self._after_id: # Cancel any leftover actions
            self.after_cancel(self._after_id)
            self._after_id = None

        self.update_display()
        self.update_buttons()

        # If AI starts first in AI mode, trigger its turn immediately
        if self.controller.game.mode == 'AI' and \
           self.controller.game.turn == 2 and \
           self.controller.game.total_moves == 0:
             self.computer_turn()
        elif self.controller.game.current_state and self.controller.game.current_state.terminal():
             self.update_buttons() # Ensure buttons disabled if game is already over

    def start_shaking_number(self):
        """Initiates the number shaking animation."""
        self.shake_count = 0
        self.shake_number()

    def shake_number(self):
        """Performs one step of the shaking animation and schedules the next."""
        if self.shake_count < self.max_shakes:
            x_offset = random.randint(-self.shake_offset, self.shake_offset)
            y_offset = random.randint(-self.shake_offset, self.shake_offset)
            # Apply temporary offset
            self.current_number_label.place(relx=0.5, rely=0.4, anchor="center", x=x_offset, y=y_offset)
            self.shake_count += 1
            self.after(self.shake_delay, self.shake_number) # Schedule next step
        else:
            # Reset position after shaking
            self.current_number_label.place(relx=0.5, rely=0.4, anchor="center", x=0, y=0)