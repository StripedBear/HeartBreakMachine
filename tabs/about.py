import customtkinter


class About(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.textbox = customtkinter.CTkTextbox(self, width=426, height=450, corner_radius=8)
        self.textbox.grid(row=0, columnspan=3, padx=6, pady=[5, 20])
        self.text = 'Can find some information here:\n\nhttps://github.com/StripedBear/HeartBreakMachine\n\n\n' \
                    'Questions on use, problems and wishes to:\n' \
                    'stripedbear@tutanota.com'
        self.textbox.insert("0.0", self.text)
        self.textbox.configure(state="disabled")


