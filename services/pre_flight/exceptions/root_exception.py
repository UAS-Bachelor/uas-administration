class WrongRootException(Exception):

    def __init__(self):
        self.message = "The root element is not called requirements."
        super().__init__(self.message)
