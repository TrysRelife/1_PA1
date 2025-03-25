import customtkinter as ctk

class ResultScreen(ctk.CTkFrame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.configure(fg_color="#150B3B")
        self.create_widgets()

    def create_widgets(self):
        # Result label to display game outcome
        self.result_label = ctk.CTkLabel(
            self, 
            text="", 
            font=("Jura Bold", 30), 
            fg_color="#150B3B", 
            text_color="white"
        )
        self.result_label.pack(pady=50)

        # Button to return to the main menu
        self.btn_main_menu = ctk.CTkButton(
            self, 
            text="Main Menu", 
            command=lambda: self.controller.show_frame("main_menu"), 
            fg_color="#3D11E6", 
            text_color="white", 
            font=("Jura", 16)
        )
        self.btn_main_menu.pack(pady=20)

    def set_result(self, result, player1_score=None, player2_score=None):
        # Update the result text with scores if provided
        if player1_score is not None and player2_score is not None:
            opponent = "Player 2" if self.controller.game.mode == '1v1' else "AI"
            result_text = f"{result}\n\nPlayer 1: {player1_score}\n{opponent}: {player2_score}"
        else:
            result_text = result
        self.result_label.configure(text=result_text)

    def on_show(self):
        # Placeholder method called when the result screen is shown
        pass