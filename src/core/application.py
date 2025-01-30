from customtkinter import CTk, get_appearance_mode


class Application(CTk):

    def __init__(self, main_view,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("%d+x%d+-10+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
        self.title("Flight Time")
        self.iconbitmap(f"{__name__}\\..\\assets\\icons\\dark_favicon.ico") if get_appearance_mode() == "Dark" else self.iconbitmap(f"{__name__}\\..\\assets\\icons\\light_favicon.ico")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.view = main_view(self)

        self.view.pack(anchor="center", expand=True, fill="both")
