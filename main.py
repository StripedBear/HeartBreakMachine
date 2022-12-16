import customtkinter
from tabs import login, parser, base, subscriber, heart_breaker, about
from action_part.sadtool import program_end


class MainWindow(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Heartbreak Machine')
        self.geometry('450x550')
        self.tab_names = ["Authorization", "Base", "Parser", "Heart Breaker", "Subscriber", "About"]
        self.tabview = customtkinter.CTkTabview(self, width=450, height=530)
        self.tabview.pack()

        [self.tabview.add(tab) for tab in self.tab_names]

        login.Authorization(self.tabview.tab("Authorization")).pack(fill='both', expand=True)
        base.Base(self.tabview.tab("Base")).pack(fill='both', expand=True)
        parser.Parser(self.tabview.tab("Parser")).pack(fill='both', expand=True)
        heart_breaker.HB(self.tabview.tab("Heart Breaker")).pack(fill='both', expand=True)
        subscriber.Subscriber(self.tabview.tab("Subscriber")).pack(fill='both', expand=True)
        about.About(self.tabview.tab("About")).pack(fill='both', expand=True)

        for item in self.tab_names:
            customtkinter.CTkLabel(self.tabview.tab(item),
                                   text='Heartbreak Machine v.0.1 by StripedBear', font=('Arial', 10)).pack()


def close_window():
    program_end()
    program.destroy()


if __name__ == '__main__':
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    program = MainWindow()
    program.protocol('WM_DELETE_WINDOW', close_window)
    program.mainloop()
