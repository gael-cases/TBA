class Item():

    # Define the constructor.
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return self.name + " : " + self.description + ". Poids : " + str(self.weight) + " kg"