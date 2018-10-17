class Track:
    def __init__(self, name, length, number, id=0):
        self.name = name
        self.length = length
        self.number = number
        self.id = id

    def print_self(self):
        print("id: ", self.id)
        print("name: ", self.name)
        print("length: ", self.length)
        print("number: ", self.number)
