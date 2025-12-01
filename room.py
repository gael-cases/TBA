# Define the Room class.

class Room:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
    
    def get_exit(self, direction):

        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        if not self.inventory:
            return "\nIl n'y a aucun objet ici.\n"

        lines = ["La pièce contient :"]
        for item in self.inventory.values():
            lines.append(f"    - {item.name} : {item.description}")
        return "\n" + "\n".join(lines) + "\n"