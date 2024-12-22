

class BadEmail(Exception):
    def __init__(self, message="Email указан в неверном формате."):
        self.message = message