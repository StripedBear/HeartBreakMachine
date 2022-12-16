from tkinter import END, filedialog
import customtkinter


class Base(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.base = []
        self.init_ui()

    def init_ui(self):
        self.add_entry = customtkinter.CTkEntry(self, width=240)
        self.add_entry.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.add_button = customtkinter.CTkButton(self, text='Add', command=self.add_target)
        self.add_button.grid(row=0, column=2)
        self.basebox = customtkinter.CTkTextbox(self, corner_radius=8, width=240)
        self.basebox.grid(row=1, column=0, columnspan=2, rowspan=6)
        self.basebox.configure(state="disabled")
        self.basebox_scrollbar = customtkinter.CTkScrollbar(self, command=self.basebox.yview)
        self.basebox_scrollbar.grid(row=1, column=1, rowspan=6, padx=[45, 0])
        self.basebox.configure(yscrollcommand=self.basebox_scrollbar.set)
        self.open_file = customtkinter.CTkButton(self, text='Load', command=self.load_db)
        self.open_file.grid(row=1, column=2)
        self.get_from_parser = customtkinter.CTkButton(self, text='Get from Parser', command=self.getfrom_parser)
        self.get_from_parser.grid(row=2, column=2)
        self.to_parser_button = customtkinter.CTkButton(self, text='To Parser',
                                                        command=lambda: self.send_to_action('parse', 'Parser'))
        self.to_parser_button.grid(row=4, column=2, pady=[7, 0])
        self.to_hb_button = customtkinter.CTkButton(self, text='To HeartBreaker',
                                                    command=lambda: self.send_to_action('hb', 'Heart Breaker'))
        self.to_hb_button.grid(row=5, column=2)
        self.to_subscriber_button = customtkinter.CTkButton(self,
                                                            text='To Subscriber',
                                                            command=lambda: self.send_to_action('subscribe',
                                                                                                'Subscriber'))
        self.to_subscriber_button.grid(row=6, column=2)
        self.clear_button = customtkinter.CTkButton(self, text='Clear', command=self.clear_db)
        self.clear_button.grid(row=7, column=0, pady=[20, 5])
        self.rm_dublicat_button = customtkinter.CTkButton(self, text='Remove duplicates', command=self.rm_dublicates)
        self.rm_dublicat_button.grid(row=8, column=0, pady=[5, 0])
        self.textbox = customtkinter.CTkTextbox(self, width=390, height=60, corner_radius=8)
        self.textbox.grid(row=9, columnspan=3, padx=[20, 0], pady=[41, 20])
        self.textbox.configure(state="disabled")

    def update_box(self, text, box, clean=True):
        box.configure(state="normal")
        if clean:
            box.delete('0.0', END)
            box.insert("0.0", text)
        else:
            box.insert(END, text)
        box.configure(state="disabled")

    def add_target(self):
        target = self.add_entry.get()
        if len(target) > 0:
            self.base.append(target)
            self.add_entry.delete(0, END)
            self.update_box(f"{target}\n", self.basebox, clean=False)
            self.update_box(f'Added {target}. Size is {len(self.base)}', self.textbox)

    def load_db(self):
        old_len = len(self.base)
        filepath = filedialog.askopenfilename()
        if filepath != "":
            with open(filepath, "r") as f:
                [self.base.append(i.rstrip()) for i in f.readlines()]
        self.update_box(f'Added to DB: {len(self.base) - old_len} targets. Size is {len(self.base)}', self.textbox)
        [self.update_box(f"{item}\n", self.basebox, clean=False) for item in self.base]

    def clear_db(self):
        self.base.clear()
        self.update_box('', self.basebox)
        self.update_box("Done! DB is EMPTY.", self.textbox)

    def rm_dublicates(self):
        new_list = list(set(self.base))
        self.base.clear()
        [self.base.append(i) for i in new_list]
        self.update_box('Duplicates removed', self.textbox)
        [self.update_box(f"{item}\n", self.basebox, clean=False) for item in self.base]

    def getfrom_parser(self):
        with open("DB/parsed") as f:
            object = [item.rstrip() for item in f.readlines()]
        if len(object) > 0:
            self.base += object
            self.update_box('Added {len(object)} targets from Parser. Size is {len(self.base)}', self.textbox)
            [self.update_box(f"{item}\n", self.basebox, clean=False) for item in object]
        else:
            self.update_box('Parsed DB is EMPTY', self.textbox)

    def send_to_action(self, filename, tabname):
        if len(self.base) > 0:
            with open(f'DB/{filename}', 'w') as f:
                [f.write(item + '\n') for item in self.base]
            self.update_box(f'Added {len(self.base)} targets to {tabname}.', self.textbox)
        else:
            self.update_box('DB is EMPTY!', self.textbox)
