# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
    
    # Define the move method.
    def move(self, direction):
        direct = {'N', 'S', 'O', 'E', 'U', 'D'}
        if direction in direct : 
            # Get the next room from the exits dictionary of the current room.
            self.history.append(self.current_room)
            next_room = self.current_room.exits[direction]
           

            # If the next room is None, print an error message and return False.
            if next_room is None:
                print("\nAucune porte dans cette direction !\n")
                return False

        
            # Set the current room to the next room.
            self.current_room = next_room
            print(self.current_room.get_long_description())
            return True
            
        else:
            print("\n Direction inconnue.\n")
            return False

    def get_history(self):
        if not self.history:
            return ""
        lines = ["Vous avez déja visité les pièces suivantes:"]
        for r in self.history:
            lines.append(f"    - {r.description}")
        return "\n" + "\n".join(lines) + "\n"

    def get_inventory(self):
        if not self.inventory:
            return ""
        lines = ["Vous disposez des items suivants"]
        for item in self.inventory:
            lines.append(f"    - {item}")
        return "\n" + "\n".join(lines) + "\n"
        
        

    