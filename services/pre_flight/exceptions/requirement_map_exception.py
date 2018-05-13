class NoSafetyZoneOnMapException(Exception):

    def __init__(self):
        self.message = "The map requirement must have a safety zone size!"
        super().__init__(self.message)


class MapNotChildOfRoot(Exception):

    def __init__(self, parent):
        self.message = "The map requirement can only be a child of root not \"" + parent + "\"."
        super().__init__(self.message)
