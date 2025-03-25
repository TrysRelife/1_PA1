import customtkinter as ctk

class GameScreen(ctk.CTkFrame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3C")
        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Top frame for scores and turn indicator
        self.top_frame = ctk.CTkFrame(self, fg_color="#150B3C", height=60)
        self.top_frame.place(relx=0.5, rely=0.0, anchor="n", relwidth=1.0)
        
        # Player 1 score label
        self.score_label_1 = ctk.CTkLabel(self.top_frame, text="Player: 0", font=("Jura", 12),
                                         fg_color="#150B3C", text_color="white")
        self.score_label_1.place(relx=0.02, rely=0.5, anchor="w")
        
        # Player 2 or AI score label
        self.score_label_2 = ctk.CTkLabel(self.top_frame, text="AI: 0", font=("Jura", 12),
                                         fg_color="#150B3C", text_color="white")
        self.score_label_2.place(relx=0.98, rely=0.5, anchor="e")

        # Turn indicator label
        self.turn_label = ctk.CTkLabel(self.top_frame, text="YOUR TURN", font=("Jura Bold", 28),
                                      fg_color="#150B3C", text_color="white")
        self.turn_label.place(relx=0.5, rely=0.5, anchor="center")

        # Current number display
        self.current_number_label = ctk.CTkLabel(self, text="0", font=("Jura Bold", 100),
                                                fg_color="#150B3C", text_color="white")
        self.current_number_label.place(relx=0.5, rely=0.4, anchor="center")

        # Bank display
        self.bank_label = ctk.CTkLabel(self, text="Bank: 0", font=("Jura Bold", 32),
                                      fg_color="#150B3C", text_color="white")
        self.bank_label.place(relx=0.5, rely=0.55, anchor="center")

        # Last move indicator
        self.last_move_label = ctk.CTkLabel(self, text="Last move: -", font=("Jura", 12),
                                          fg_color="#150B3C", text_color="white")
        self.last_move_label.place(relx=0.02, rely=0.3, anchor="w")

        # Divide by 2 button
        self.btn_divide2 = ctk.CTkButton(self, text="÷ 2", command=lambda: self.handle_move(2),
                                         fg_color="#E77C12", text_color="white", font=("Jura", 22),
                                         width=150, height=60)
        self.btn_divide2.place(relx=0.35, rely=0.7, anchor="center")

        # Divide by 3 button
        self.btn_divide3 = ctk.CTkButton(self, text="÷ 3", command=lambda: self.handle_move(3),
                                         fg_color="#3E12E7", text_color="white", font=("Jura", 22),
                                         width=150, height=60)
        self.btn_divide3.place(relx=0.65, rely=0.7, anchor="center")

        # End game button
        self.btn_end_game = ctk.CTkButton(self, text="End Game", command=self.end_game,
                                        fg_color="#5C1500", text_color="white", font=("Jura", 22),
                                        width=250, height=70)
        self.btn_end_game.place(relx=0.5, rely=0.85, anchor="center")

    def on_resize(self, event):
        # Adjust font sizes based on window width
        width = self.winfo_width()
        new_font_size_current = max(20, int(width / 15))
        new_font_size_turn_bank = max(12, int(width / 40))
        new_font_size_scores = max(8, int(width / 60))
        
        self.current_number_label.configure(font=("Jura Bold", new_font_size_current))
        self.turn_label.configure(font=("Jura Bold", new_font_size_turn_bank))
        self.bank_label.configure(font=("Jura Bold", new_font_size_turn_bank))
        self.score_label_1.configure(font=("Jura", new_font_size_scores))
        self.score_label_2.configure(font=("Jura", new_font_size_scores))
        self.last_move_label.configure(font=("Jura", new_font_size_scores))

    def handle_move(self, divisor):
        # Handle player move and update UI
        self.controller.game.make_move(divisor)
        self.last_move_label.configure(text=f"Last move: /{divisor}")
        self.update_display()
        self.update_buttons()

        if self.controller.game.mode == 'AI':
            self.computer_turn()

    def computer_turn(self):
        # Disable buttons and let AI make a move
        self.btn_divide2.configure(state="disabled")
        self.btn_divide3.configure(state="disabled")
        self.after(1000, self.perform_computer_move)

    def perform_computer_move(self):
        # Execute AI move and update UI
        divisor = self.controller.game.computer_move()
        if divisor != None:
            self.last_move_label.configure(text=f"Last move: /{divisor}")
        self.on_show()

    def update_display(self):
        # Update scores, current number, and bank
        state = self.controller.game.get_game_state()
        current_number = state.n if state.n else 0

        self.current_number_label.configure(text=f"{current_number:n}" if current_number > 0 else "0")
        self.bank_label.configure(text=f"Bank: {state.b}")

        if self.controller.game.mode == '1v1':
            self.score_label_1.configure(text=f"PLAYER 1: {state.pp if state.original_turn == 1 else state.cp}")
            self.score_label_2.configure(text=f"PLAYER 2: {state.cp if state.original_turn == 1 else state.pp}")
            self.turn_label.configure(text=f"PLAYER {'1' if self.controller.game.turn == 1 else '2'}'S TURN")
        else:
            self.score_label_1.configure(text=f"PLAYER: {state.pp if state.original_turn == 1 else state.cp}")
            self.score_label_2.configure(text=f"AI: {state.cp if state.original_turn == 1 else state.pp}")
            self.turn_label.configure(text=f"{'YOUR' if self.controller.game.turn == 1 else 'AI'} TURN")

    def update_buttons(self):
        # Enable/disable buttons based on current number
        state = self.controller.game.get_game_state()
        current_number = state.n

        self.btn_divide2.configure(state="normal" if current_number % 2 == 0 else "disabled")
        self.btn_divide3.configure(state="normal" if current_number % 3 == 0 else "disabled")

        if self.controller.game.mode == 'AI' and self.controller.game.turn == 2:
            self.btn_divide2.configure(state="disabled")
            self.btn_divide3.configure(state="disabled")

    def end_game(self):
        # Display results screen
        state = self.controller.game.get_game_state()
        p1 = state.pp if state.original_turn == 1 else state.cp
        p2 = state.cp if state.original_turn == 1 else state.pp
        if self.controller.game.mode == '1v1':    
            winner = "PLAYER 1 WINS" if p1 > p2 else "PLAYER 2 WINS" if p2 > p1 else "DRAW"
        else:
            winner = "PLAYER WINS" if p1 > p2 else "AI WINS" if p2 > p1 else "DRAW"

        self.controller.show_result(winner, p1, p2)

    def on_show(self):
        # Update UI when screen is shown
        self.update_display()
        self.update_buttons()