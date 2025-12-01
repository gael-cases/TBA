class Player():

    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 10
        self.rewards = []
        self.beamer_room = None

    def move(self, direction):
        direct = {'N', 'S', 'O', 'E', 'U', 'D'}
        
        if direction not in direct:
            print("\nDirection inconnue.\n")
            return False
        
        next_room = self.current_room.exits[direction]

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        self.history.append(self.current_room)

        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    def get_history(self):
        if not self.history:
            return ""
        lines = ["Vous avez déjà visité les pièces suivantes:"]
        for r in self.history:
            lines.append(f"    - {r.name}")
        return "\n" + "\n".join(lines) + "\n"

    def get_inventory(self):
        if not self.inventory:
            return ""
        lines = ["Vous disposez des items suivants :"]
        for item in self.inventory.values():
            lines.append(f"    - {item.name} : {item.description}")
        return "\n" + "\n".join(lines) + "\n"