class Person:

    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences

    def print(self):
        print(self.name + " has preferences ")
        print(self.preferences)