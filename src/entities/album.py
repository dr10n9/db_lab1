class Album:
    def __init__(self, name, tracksCount, id = 0):
        self.name = name
        self.tracksCount = tracksCount
        self.id = 0

    def print_self(self):
        print("id: ", self.id)
        print("Name: ", self.name)
        print("TracksCount: ", self.tracksCount)
        
