from tkinter import END
import customtkinter
from action_part.sadtool import *


class Subscriber(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

        self.subscriber_db = []
        self.boolean = None

    def init_ui(self):
        self.delay_label = customtkinter.CTkLabel(self, text="Delay")
        self.delay_label.grid(row=1, column=0, pady=[30, 10])
        self.delay_spinbox = customtkinter.CTkEntry(self)
        self.delay_spinbox.grid(row=1, column=1, pady=[30, 10])
        self.amount_label = customtkinter.CTkLabel(self, text="Amount")
        self.amount_label.grid(row=2, column=0, padx=[5, 0])
        self.amount_spinbox = customtkinter.CTkEntry(self)
        self.amount_spinbox.grid(row=2, column=1)
        self.basebox = customtkinter.CTkTextbox(self, corner_radius=8, width=235)
        self.basebox.grid(row=3, column=0, columnspan=2, rowspan=6, padx=20, pady=[20, 0])
        self.basebox.configure(state="disabled")
        self.basebox_scrollbar = customtkinter.CTkScrollbar(self, command=self.basebox.yview)
        self.basebox_scrollbar.grid(row=3, column=1, rowspan=6, padx=[140, 0], pady=[20, 0])
        self.basebox.configure(yscrollcommand=self.basebox_scrollbar.set)
        self.go_button = customtkinter.CTkButton(self, text='Start', command=self.loadbase_subscriber)
        self.go_button.grid(row=3, column=2, pady=[15, 0])
        self.stop_button = customtkinter.CTkButton(self, text='Stop', command=self.stop_subscriber)
        self.stop_button.grid(row=4, column=2, pady=[0, 90])
        self.textbox = customtkinter.CTkTextbox(self, width=390, height=60, corner_radius=8)
        self.textbox.grid(row=12, columnspan=3, padx=[20, 0], pady=[78, 20])
        self.textbox.configure(state="disabled")

    def update_box(self, text, box, clean=True):
        box.configure(state="normal")
        if clean:
            box.delete('0.0', END)
            box.insert("0.0", text)
        else:
            box.insert(END, text)
        box.configure(state="disabled")

    def start_subscriber(self):
        delay = self.delay_spinbox.get()
        if len(self.subscriber_db) > 0:
            subscriber_by_base(self.subscriber_db[0])
            self.update_box(f'Delay:{delay} sec. subscribed to {self.subscriber_db[0]}', self.textbox)
            self.subscriber_db.remove(self.subscriber_db[0])
            self.update_box('', self.basebox)
            [self.update_box(f"{item}\n", self.basebox, clean=False) for item in self.subscriber_db]
            self.boolean = self.after(int(f'{delay}000'), self.start_subscriber)

    def stop_subscriber(self):
        if self.boolean is not None:
            self.after_cancel(self.boolean)
            self.update_box('Stopped', self.textbox)
            self.boolean = None

    def loadbase_subscriber(self):
        self.subscriber_db.clear()
        with open('DB/subscribe') as f:
            for item in f.readlines():
                self.subscriber_db.append(item.rstrip())
        if (amount := int(self.amount_spinbox.get())) == 0:
            amount = len(self.subscriber_db)
        self.update_box('DB is loading...', self.textbox)
        [self.update_box(f"{item}\n", self.basebox) for item in self.subscriber_db]
        self.subscriber_db = self.subscriber_db[0:amount]
        self.start_subscriber()
