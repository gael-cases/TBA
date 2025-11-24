# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        # Dictionnaire nom_item -> Item
        self.inventory = {}
        # Dictionnaire nom_pnj -> Character
        self.characters = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        # description utilisée partout (go, début du jeu, etc.)
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """
        Retourne une description textuelle des objets présents dans la salle.

        ⚠️ IMPORTANT :
        - self.inventory est un dict {nom_item: Item}
        - on boucle donc sur .values() pour récupérer les objets.
        """
        if not self.inventory:
            return "\nIl n'y a aucun objet ici.\n"

        lines = ["La pièce contient :"]
        # on parcourt les objets (instances de Item)
        for item in self.inventory.values():
            lines.append(f"    - {item.name} : {item.description}")
        return "\n" + "\n".join(lines) + "\n"
