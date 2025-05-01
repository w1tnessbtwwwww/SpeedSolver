

class BadColor(Exception):
    def __init__(self, message="Цвет не является HTML."):
        self.message = message