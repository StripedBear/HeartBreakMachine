from tkinter import filedialog
from tkinter import *
import customtkinter
from action_part.sadtool import *


class Parser(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.parsed = []
        self.base = []
        self.init_ui()

    def init_ui(self):
        self.parsers = {"parse broken hearts": parsing_likers, "parse followers": parsing_followers,
                        "parse posts by keywords": prs_posts_kw}
        self.title_parser = customtkinter.CTkLabel(self, text="Choose Parser", font=(0, 10,))
        self.title_parser.grid(row=0, column=0, padx=[0, 80], pady=[10, 0])
        self.parsers_combobox = customtkinter.CTkComboBox(self, values=list(self.parsers),
                                                          width=240, fg_color="#006699")
        self.parsers_combobox.grid(row=1, column=0, columnspan=2, padx=[15, 20], pady=[0, 20])
        self.basebox = customtkinter.CTkTextbox(self, corner_radius=8, width=235)
        self.basebox.grid(row=3, column=0, columnspan=2, rowspan=6)
        self.basebox.configure(state="disabled")
        self.basebox_scrollbar = customtkinter.CTkScrollbar(self, command=self.basebox.yview)
        self.basebox_scrollbar.grid(row=3, column=1, rowspan=6, padx=[45, 0])
        self.basebox.configure(yscrollcommand=self.basebox_scrollbar.set)
        self.go_parse = customtkinter.CTkButton(self, text='Start', command=self.prepare_base)
        self.go_parse.grid(row=3, column=2)
        self.stop_parse = customtkinter.CTkButton(self, text='Stop', command=self.stop_action)
        self.stop_parse.grid(row=4, column=2, pady=[0, 85])
        self.save_parsed = customtkinter.CTkButton(self, text='Save', command=self.save_parsed)
        self.save_parsed.grid(row=10, column=0, pady=[20, 5], padx=[0, 10])
        self.clear_parsed = customtkinter.CTkButton(self, text='Clear', command=self.clear_parsed)
        self.clear_parsed.grid(row=11, column=0, padx=[0, 10], pady=[5, 5])
        self.textbox = customtkinter.CTkTextbox(self, width=390, height=60, corner_radius=8)
        self.textbox.grid(row=12, columnspan=3, padx=[20, 0], pady=[18, 20])
        self.textbox.configure(state="disabled")

    def update_box(self, text, box, clean=True):
        box.configure(state="normal")
        if clean:
            box.delete('0.0', END)
            box.insert("0.0", text)
        else:
            box.insert(END, text)
        box.configure(state="disabled")

    def parse(self):
        try:
            object = self.parsers.get(self.parsers_combobox.get())(self.base[0])
            [self.parsed.append(item) for item in object]
            self.update_box(f'Parsed: {self.base[0]}', self.textbox)
            self.base.remove(self.base[0])
            self.update_box('', self.basebox)
            [self.update_box(f"{item}\n", self.basebox, clean=False) for item in self.parsed]
            if len(self.base) > 0:
                self.boolean = self.after(100, self.parse)
            else:
                self.update_box(f'Done! Parsed: {len(self.parsed)} targets', self.textbox)
        except Exception as e:
            self.update_box(f'Error: {e}', self.textbox)

    def prepare_base(self):
        self.base.clear()
        with open('DB/parse') as f:
            [self.base.append(item.rstrip()) for item in f.readlines()]
        if len(self.base) > 0:
            self.parse()
            with open('DB/parsed', 'w') as f:
                [f.write(f'{item}\n') for item in self.parsed]
        else:
            self.update_box('Error: DB is EMPTY!', self.textbox)

    def stop_action(self):
        if self.boolean is not None:
            self.after_cancel(self.boolean)
            self.update_box('Stopped', self.textbox)
            self.boolean = None

    def clear_parsed(self):
        self.parsed.clear()
        self.base.clear()
        self.update_box('', self.basebox)
        self.update_box('List is EMPTY', self.textbox)

    def save_parsed(self):
        filepath = filedialog.asksaveasfilename()
        if filepath != "":
            with open(filepath, "w") as f:
                [f.write(f"{i}\n") for i in self.parsed]
            self.update_box('File is saved', self.textbox)
