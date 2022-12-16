import os
import shutil
from tkinter import END

import customtkinter
from action_part.sadtool import *


class Authorization(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.login_entry = customtkinter.CTkEntry(self, width=180, placeholder_text="Login")
        self.login_entry.pack(anchor='center', pady=[60, 5])
        self.password_entry = customtkinter.CTkEntry(self, width=180, placeholder_text="Password")
        self.password_entry.pack(anchor='center', pady=[5, 10])
        self.check_auth = customtkinter.CTkButton(self, text='Check', command=self.checking_auth)
        self.check_auth.pack(anchor='center', pady=[10, 5])
        self.check_auth = customtkinter.CTkButton(self, text='Log In', fg_color='green', command=self.login)
        self.check_auth.pack(anchor='center', pady=[5, 5])
        self.clean_auth = customtkinter.CTkButton(self, text='Clear', command=self.auth_clean)
        self.clean_auth.pack(anchor='center', pady=[5, 5])
        self.textbox = customtkinter.CTkTextbox(self, width=390, height=60, corner_radius=8)
        self.textbox.pack(anchor='center', pady=[140, 20])
        self.textbox.configure(state="disabled")

    def update_textbox(self, text):
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', END)
        self.textbox.insert("0.0", text)
        self.textbox.configure(state="disabled")

    def checking_auth(self):
        if check() == 'https://grustnogram.ru/dashboard/':
            self.update_textbox('ok')
        else:
            self.update_textbox('not ok')

    def login(self):
        login_data = self.login_entry.get()
        password_data = self.password_entry.get()
        output = auth(login_data, password_data)
        self.update_textbox(output)

    def auth_clean(self):
        shutil.rmtree(os.path.abspath('browser_data'))
        self.update_textbox('Cleared')
