from enum import Enum

class Genres(Enum):
    ROCK = 'rock'
    PUNK = 'punk'
    RAP = 'rap'
    CHANSON = 'chanson'
    CLASSIC = 'classic'

class Band:
    def __init__(self, name, genre: Genres, exists, id=0):
        self.name = name
        self.genre = genre.value
        self.exists = exists
        self.id = id

    def print_self(self):
        print("id: ", self.id)
        print("name: ", self.name)
        print("genre: ", self.genre)
        print("exists: ", self.exists)

