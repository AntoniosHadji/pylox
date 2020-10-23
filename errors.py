from token_class import Token


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__()
        self.token = token
        self.message = message
