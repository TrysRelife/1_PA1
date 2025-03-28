import customtkinter as ctk
import random # For the number shaking animation effect

class GameScreen(ctk.CTkFrame):
    """UI Frame for the main game play area."""

    def __init__(self, controller):
        """Initializes the game screen UI elements and animation variables."""
        super().__init__(controller)
        self.controller = controller # Reference to the main app controller
        self.configure(fg_color="#150B3C") # Background color
        self.create_widgets()
        self.bind("<Configure>", self.on_resize) # Bind resize event for dynamic font sizing
        self._after_id = None # Stores ID for pending 'after' calls (e.g., AI delay)

        # --- Shaking Animation Variables ---
        self.shake_offset = 5    # Max pixel offset during shake
        self.shake_delay = 50    # Milliseconds between shake movements
        self.shake_count = 0     # Current shake step
        self.max_shakes = 6      # Total number of shake movements per animation

    def create_widgets(self):
        """Creates and arranges all UI widgets on the game screen."""

        # --- Top Frame: Scores and Turn Indicator ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.top_frame.place(relx=0.5, rely=0.0, anchor="n", relwidth=1.0)

        self.score_label_1 = ctk.CTkLabel(self.top_frame, text="Player: 0", font=("Jura", 12), text_color="white")
        self.score_label_1.place(relx=0.02, rely=0.5, anchor="w") # Left aligned

        self.score_label_2 = ctk.CTkLabel(self.top_frame, text="AI: 0", font=("Jura", 12), text_color="white")
        self.score_label_2.place(relx=0.98, rely=0.5, anchor="e") # Right aligned

        self.turn_label = ctk.CTkLabel(self.top_frame, text="YOUR TURN", font=("Jura Bold", 28), text_color="white")
        self.turn_label.place(relx=0.5, rely=0.5, anchor="center") # Centered

        # --- Main Game Area ---
        self.current_number_label = ctk.CTkLabel(self, text="0", font=("Jura Bold", 100), text_color="white")
        self.current_number_label.place(relx=0.5, rely=0.4, anchor="center") # Central number display

        self.bank_label = ctk.CTkLabel(self, text="Bank: 0", font=("Jura Bold", 32), text_color="white")
        self.bank_label.place(relx=0.5, rely=0.55, anchor="center") # Bank display below number

        self.last_move_label = ctk.CTkLabel(self, text="Last move: -", font=("Jura", 12), text_color="white")
        self.last_move_label.place(relx=0.02, rely=0.3, anchor="w") # Display last division made

        # --- Action Buttons ---
        self.btn_divide2 = ctk.CTkButton(self, text="÷ 2", command=lambda: self.handle_move(2),
                                         fg_color="#E77C12", text_color="white", font=("Jura", 22),
                                         width=150, height=60, corner_radius=10, hover_color="#D6700F")
        self.btn_divide2.place(relx=0.35, rely=0.7, anchor="center") # Divide by 2 button

        self.btn_divide3 = ctk.CTkButton(self, text="÷ 3", command=lambda: self.handle_move(3),
                                         fg_color="#3E12E7", text_color="white", font=("Jura", 22),
                                         width=150, height=60, corner_radius=10, hover_color="#360FC4")
        self.btn_divide3.place(relx=0.65, rely=0.7, anchor="center") # Divide by 3 button

        self.btn_end_game = ctk.CTkButton(self, text="End Game / Show Result", command=self.end_game,
                                        fg_color="#5C1500", text_color="white", font=("Jura", 20),
                                        width=250, height=50, hover_color="#4A1000")
        self.btn_end_game.place(relx=0.5, rely=0.85, anchor="center") # Button to manually end/view results

    def on_resize(self, event):
        """Adjusts font sizes dynamically based on window dimensions."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Calculate responsive font sizes with min/max caps
        base_width = 800
        scale_factor = width / base_width
        current_font_size = max(30, min(120, int(height * 0.15))) # Large number font
        turn_bank_font_size = max(18, min(40, int(scale_factor * 32))) # Turn/Bank font
        scores_font_size = max(10, min(20, int(scale_factor * 14))) # Score/LastMove font
        button_font_size = max(14, min(26, int(scale_factor * 22))) # Divide buttons font
        end_button_font_size = max(14, min(22, int(scale_factor * 20))) # End game button font

        # Apply the new font sizes to the widgets
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
        """Processes a player's move (triggered by button press)."""
        
        self.controller.game.make_move(divisor) # Update game logic state
        self.last_move_label.configure(text=f"Last move: / {divisor}") # Update UI
        self.update_display() # Refresh all UI elements
        self.start_shaking_number() # Trigger visual feedback

        # Check if the move ended the game
        if self.controller.game.current_state.terminal():
            self.update_buttons() # Disable buttons
            self.after(500, self.end_game) # Show results after a short delay
            return

        self.update_buttons() # Update button states for the next turn

        # If playing against AI and it's now the AI's turn, trigger AI move
        if self.controller.game.mode == 'AI' and self.controller.game.turn == 2:
            self.computer_turn()

    def computer_turn(self):
        """Initiates the AI's turn, showing a thinking message and disabling buttons."""
        self.turn_label.configure(text="AI THINKING...") # Update turn indicator
        self.btn_divide2.configure(state="disabled") # Disable player input
        self.btn_divide3.configure(state="disabled")

        # Cancel any previous pending 'after' calls to avoid duplicate AI moves
        if self._after_id:
            self.after_cancel(self._after_id)

        # Schedule the actual AI calculation after a short delay (for visual feedback)
        self._after_id = self.after(1000, self.perform_computer_move)

    def perform_computer_move(self):
        """Executes the AI move calculation and updates the UI."""

        # Double-check if game ended while waiting for the 'after' delay
        if self.controller.game.current_state.terminal():
             self.end_game()
             return

        divisor = self.controller.game.computer_move() # Get AI's chosen move from game logic
        self.last_move_label.configure(text=f"Last move: / {divisor}") # Update UI
        self.update_display() # Refresh all elements
        self.start_shaking_number() # Trigger visual feedback

        # Check if AI's move ended the game
        if self.controller.game.current_state.terminal():
            self.update_buttons() # Disable buttons
            self.after(500, self.end_game) # Show results after delay
        else:
            self.update_buttons() # Re-enable player buttons for their turn
            
        self._after_id = None # Clear the pending task ID

    def update_display(self):
        """Refreshes all UI elements to reflect the current game state."""
        state = self.controller.game.get_game_state()
        if not state: return # Do nothing if game state isn't ready

        # Update number and bank displays
        current_number = state.n
        self.current_number_label.configure(text=f"{current_number:,}" if current_number > 0 else "0")
        self.bank_label.configure(text=f"Bank: {state.b}")

        # Map internal scores (pp, cp) to display labels (P1/P2 or Player/AI)
        # This part correctly gets P1/P2 score based on who started
        p1_score = state.pp if state.original_turn == 1 else state.cp
        p2_score = state.cp if state.original_turn == 1 else state.pp

        # Update score labels and turn indicator based on game mode
        if self.controller.game.mode == '1v1':
            self.score_label_1.configure(text=f"PLAYER 1: {state.pp}")
            self.score_label_2.configure(text=f"PLAYER 2: {state.cp}")
            player_turn_text = '1' if self.controller.game.turn == 1 else '2'
            turn_text = f"PLAYER {player_turn_text}'S TURN" if not state.terminal() else "GAME OVER"
        else: # AI Mode
            # Determine which score belongs to the human player and which to the AI
            if state.original_turn == 1: # Human started as P1
                player_actual_score = p1_score
                ai_actual_score = p2_score
            else: # AI started as P1 (Human is P2)
                player_actual_score = p2_score
                ai_actual_score = p1_score

            # Assign scores to the correct labels
            self.score_label_1.configure(text=f"PLAYER: {player_actual_score}")
            self.score_label_2.configure(text=f"AI: {ai_actual_score}")

            turn_text = "YOUR TURN" if self.controller.game.turn == 1 else "AI TURN"
            if state.terminal():
                 turn_text = "GAME OVER"
            elif self.controller.game.turn == 2 and self._after_id: # Show thinking if AI turn is pending
                turn_text = "AI THINKING..."

        self.turn_label.configure(text=turn_text)

    def update_buttons(self):
        """Enables/disables the division buttons based on number divisibility and whose turn it is."""
        state = self.controller.game.get_game_state()
        # Disable all if game is over or state not ready
        if not state or state.terminal():
            self.btn_divide2.configure(state="disabled")
            self.btn_divide3.configure(state="disabled")
            return

        current_number = state.n
        # Determine if the human player should be able to interact
        is_player_turn = True
        if self.controller.game.mode == 'AI' and self.controller.game.turn == 2:
            is_player_turn = False # Disable buttons during AI's turn

        # Enable/disable based on divisibility AND if it's the player's turn
        self.btn_divide2.configure(state="normal" if current_number % 2 == 0 and is_player_turn else "disabled")
        self.btn_divide3.configure(state="normal" if current_number % 3 == 0 and is_player_turn else "disabled")

    def end_game(self):
        """Cleans up pending actions and transitions to the result screen."""
        # Cancel any pending AI move calculation
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        self.last_move_label.configure(text="Last move: -") # Reset for potential next game
        self.controller.record_and_show_result() # Tell controller to show results

    def on_show(self):
        """Called when the GameScreen becomes visible. Sets up initial display and AI turn if needed."""

        self.update_display() # Ensure UI is current
        self.update_buttons() # Set initial button states

        # --- Trigger AI's first move if AI starts ---
        if self.controller.game.mode == 'AI' and \
           self.controller.game.turn == 2 and \
           self.controller.game.total_moves == 0: # Check if it's the very start of the game
             self.computer_turn()
        elif self.controller.game.current_state and self.controller.game.current_state.terminal():
             # Ensure buttons are disabled if the game loaded is already finished
             self.update_buttons()

    def start_shaking_number(self):
        """Initiates the number label shaking animation."""
        self.shake_count = 0 # Reset shake counter
        self.shake_number() # Start the animation loop

    def shake_number(self):
        """Performs one step of the shaking animation and schedules the next."""
        if self.shake_count < self.max_shakes:
            # Calculate random offset
            x_offset = random.randint(-self.shake_offset, self.shake_offset)
            y_offset = random.randint(-self.shake_offset, self.shake_offset)
            # Apply temporary offset using place's relative positioning
            self.current_number_label.place(relx=0.5, rely=0.4, anchor="center", x=x_offset, y=y_offset)
            self.shake_count += 1
            # Schedule the next shake movement
            self.after(self.shake_delay, self.shake_number)
        else:
            # Reset position to center after the animation completes
            self.current_number_label.place(relx=0.5, rely=0.4, anchor="center", x=0, y=0)