class IMIConnectionError(Exception):
    def __init__(self, message):
        self.message = message

class IMIAuthError(Exception):
    def __init__(self, message):
        self.message = message

class MoveError(Exception):
    def __init__(self, message):
        self.message = message

class CreateError(Exception):
    def __init__(self, message):
        self.message = message
