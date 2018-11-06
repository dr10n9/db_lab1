class Track:
    def __init__(self, name, length, id=0):
        self.name = name
        self.length = length
        self.id = id

    def print_self(self):
        print("id: ", self.id)
        print("name: ", self.name)
        print("length: ", self.length)
