import time


class TimerModel:

    def __init__(self, duration: int = 0):
        """Initializes the timer with a specific duration in seconds."""
        self.total_duration: int = duration
        self.remaining_time: int = duration
        self.start_time: float = None
        self.running: bool = False

    def start(self):
        """Starts the countdown timer. If already running, it does nothing."""
        if self.running: return
        self.start_time = time.perf_counter()
        self.running = True

    def stop(self):
        """Stops the timer and updates the remaining time."""
        if not self.running: return
        self.remaining_time -= time.perf_counter() - self.start_time
        self.start_time = None
        self.running = False

    def resume(self):
        """Resumes the timer if it was paused."""
        if self.running or not self.remaining_time > 0: return
        self.start_time = time.perf_counter()
        self.running = True

    def reset(self):
        """Resets the timer to its initial duration."""
        self.start_time = None
        self.remaining_time = self.total_duration
        self.running = False

    def get_remaining_time(self):
        """Returns the remaining time in seconds."""
        if not self.running: return max(0, self.remaining_time)
        elapsed = time.perf_counter() - self.start_time
        return max(0, self.remaining_time - elapsed)

    def is_running(self):
        """Returns whether the timer is currently running."""
        return self.running

    def set_time(self, duration: int):
        """Sets a new duration for the timer."""
        self.total_duration = duration
        self.remaining_time = duration
        if not self.running: return
        self.start_time = time.perf_counter()
