from typing import override

from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage

from assets.sounds.beep import beep
from src.lib.base_observer import BaseObserver
from src.view_model.timer_viewmodel import TimerViewModel

class TimerView(BaseObserver, CTkFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._view_model = TimerViewModel()
        self._view_model.add_observer(self)

        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.rowconfigure((0, 1, 2), weight=1, uniform="row")
        self.pack( anchor="center", expand=True, fill="both" )
        self.timer_label = CTkLabel(self, text="", font=("Arial", 200))
        self.timer_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.round_label = CTkLabel(self, text="", font=("Arial", 100))
        self.round_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        #####  color level frame  #####
        image_frame = CTkFrame(self, fg_color='transparent')
        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.rowconfigure((0, 1, 2), weight=1)
        image_frame.grid(column=0, rowspan=3, row=0, padx=10, pady=10, sticky="nsew")
        self.full_red_image = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\full_red_rounded_square.png"), size=(200, 200))
        self.full_orange_image = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\full_orange_rounded_square.png"), size=(200, 200))
        self.full_green_image = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\full_green_rounded_square.png"), size=(200, 200))
        self.outlined_red_image = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\outlined_red_rounded_square.png"), size=(200, 200))
        self.outlined_orange_image = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\outlined_orange_rounded_square.png"), size=(200, 200))
        self.outlined_green_image = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\outlined_green_rounded_square.png"), size=(200, 200))
        self.red_icon = CTkLabel(image_frame, image=self.full_red_image, text="", font=("Arial", 200))
        self.orange_icon = CTkLabel(image_frame, image=self.full_orange_image, text="", font=("Arial", 200))
        self.green_icon = CTkLabel(image_frame, image=self.full_green_image, text="", font=("Arial", 200))
        self.red_icon.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.orange_icon.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.green_icon.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        ##### action button frame #####
        button_frame = CTkFrame(self, fg_color='transparent')
        button_frame.grid_columnconfigure((0, 1), weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.start_icon = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\light_start_icon.png"), dark_image=Image.open(f"{__name__}\\..\\assets\\images\\dark_start_icon.png"), size=(100, 100))
        self.finish_icon = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\light_finish_icon.png"), dark_image=Image.open(f"{__name__}\\..\\assets\\images\\dark_finish_icon.png"), size=(100, 100))
        self.skip_icon = CTkImage(light_image=Image.open(f"{__name__}\\..\\assets\\images\\light_skip_icon.png"), dark_image=Image.open(f"{__name__}\\..\\assets\\images\\dark_skip_icon.png"), size=(100, 100))
        self.start_stop_button = CTkButton(button_frame, image=self.start_icon, text="", font=("Arial", 100), command=lambda: self._view_model.toggle_round())
        self.start_stop_button.grid(row=0, column=0, padx=10, pady=10)
        self.stop_button = CTkButton(button_frame, image=self.skip_icon, text="", font=("Arial", 100), command=lambda: self._view_model.skip_round())
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        ##### current teams indicators #####
        teams_frame = CTkFrame(self, fg_color='transparent')
        teams_frame.grid_columnconfigure(0, weight=1)
        teams_frame.rowconfigure((0, 1), weight=1)
        teams_frame.grid(column=2, rowspan=3, row=0, padx=10, pady=10, sticky="nsew")
        self.team_one_label = CTkLabel(teams_frame, text="", font=("Arial", 150))
        self.team_one_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.team_two_label = CTkLabel(teams_frame, text="", font=("Arial", 150))
        self.team_two_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self._view_model.notify_observers()

    @override
    def update(self, **kwargs):
        self.timer_label.configure(text=f"{kwargs['remaining_time']:.0f}")
        self.team_one_label.configure(text=f"{kwargs['teams'][kwargs['wave']][0]}")
        self.team_two_label.configure(text=f"{kwargs['teams'][kwargs['wave']][1]}")
        self.round_label.configure(text=f"tour {kwargs['current_round']}")

        if kwargs['remaining_time'] == 0 or kwargs['remaining_time'] is None:
            match kwargs['stage']:
                case 0 :
                    self._view_model.set_duration(10)
                    self._view_model.next_stage()
                case 1 :
                    self._view_model.set_duration(120)
                    self._view_model.next_stage()
                case 2 :
                    self._view_model.next_stage()
                    self._view_model.set_duration(10)
                    self._view_model.next_wave()
                    if kwargs['wave'] == 1:
                        self._view_model.end_round()

        match kwargs['remaining_time']:
            case 120:
                self.green_icon.configure(image=self.full_green_image)
                self.orange_icon.configure(image=self.outlined_orange_image)
                self.red_icon.configure(image=self.outlined_red_image)
            case 30:
                self.green_icon.configure(image=self.outlined_green_image)
                self.orange_icon.configure(image=self.full_orange_image)
                self.red_icon.configure(image=self.outlined_red_image)
            case 10:
                self.green_icon.configure(image=self.outlined_green_image)
                self.orange_icon.configure(image=self.outlined_orange_image)
                self.red_icon.configure(image=self.full_red_image)
                if kwargs['is_running']:
                    beep()
            case 0:
                if kwargs['is_running']:
                    beep()

        print(kwargs)
