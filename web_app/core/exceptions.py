

class InputDataError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f'{self.message}'
