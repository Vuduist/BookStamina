class InputChecker:
    def __init__(self):
        self.errors = 0
        self.total = 0

    def check(self, reference, typed):
        self.errors = 0
        self.total = len(reference)
        for i, ch in enumerate(typed):
            if i >= len(reference) or ch != reference[i]:
                self.errors += 1
        return self.errors

    def accuracy(self):
        if self.total == 0:
            return 100.0
        return 100.0 * (self.total - self.errors) / self.total 