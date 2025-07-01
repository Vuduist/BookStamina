class Stats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chars_typed = 0
        self.errors = 0
        self.start_time = None
        self.end_time = None

    def add_typed(self, count):
        self.chars_typed += count

    def add_error(self, count):
        self.errors += count

    def set_start(self, t):
        self.start_time = t

    def set_end(self, t):
        self.end_time = t

    def get_speed(self):
        if self.start_time and self.end_time:
            minutes = (self.end_time - self.start_time) / 60
            return self.chars_typed / minutes if minutes > 0 else 0
        return 0

    def get_accuracy(self):
        total = self.chars_typed + self.errors
        return 100.0 * self.chars_typed / total if total > 0 else 100.0 