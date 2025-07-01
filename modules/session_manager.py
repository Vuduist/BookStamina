class SessionManager:
    def __init__(self):
        self.current_book = None
        self.current_position = 0
        self.settings = {}

    def set_book(self, book_title):
        self.current_book = book_title
        self.current_position = 0

    def set_position(self, pos):
        self.current_position = pos

    def get_state(self):
        return self.current_book, self.current_position 