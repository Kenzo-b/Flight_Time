import time
import threading
from src.lib.base_observable import BaseObservable, notify
from src.model.round_model import RoundModel
from src.model.timer_model import TimerModel



class TimerViewModel(BaseObservable):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._models: dict = {'timer_model':TimerModel(), 'round_model':RoundModel()}
        self.current_round = 1
        self.wave = 0
        self.stage = 0
        self.remaining_time = 0
        self.teams = self._models['round_model'].teams_order
        self.is_running = False

    def _start_timer(self):
        if not self._models['timer_model'].is_running():
            self._models['timer_model'].start()
            self.is_running = self._models['timer_model'].is_running()
            self._start_tick_loop()  # Start ticking

    def _stop_timer(self):
        self._models['timer_model'].stop()
        self.is_running = self._models['timer_model'].is_running()

    def _start_tick_loop(self):
        """Continuously update the timer and notify observers."""
        def loop():
            while self.is_running:
                time.sleep(1)  # Update every seconds
                self.remaining_time = round(self._models['timer_model'].get_remaining_time(), 0)
                self.notify_observers()
        threading.Thread(target=loop, daemon=True).start()

    def _next_round(self):
        self._models['round_model'].next_round()
        self.teams = self._models['round_model'].teams_order

    def _reset_timer(self):
        self._models['timer_model'].reset()
        self.is_running = self._models['timer_model'].is_running()
        self.remaining_time = self._models['timer_model'].get_remaining_time()

    @notify
    def start_round(self):
        if self._models['timer_model'].is_running() or self.remaining_time == 0: return
        self.current_round = self._models['round_model'].current_round
        self._start_timer()

    @notify
    def skip_round(self):
        self._models['timer_model'].stop()
        self.set_duration(10)
        self._next_round()

    @notify
    def next_wave(self):
        self.wave = (self.wave + 1) % 2

    @notify
    def next_stage(self):
        self.stage = (self.stage + 1) % 3

    @notify
    def set_duration(self, duration: int):
        self._models['timer_model'].set_time(duration)
        self.remaining_time = round(self._models['timer_model'].get_remaining_time(), 0)

    def toggle_round(self):
        self.skip_round() if self._models['timer_model'].is_running() else self.start_round()

    @notify
    def end_round(self):
        self._stop_timer()
        self._next_round()

