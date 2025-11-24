# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []

        # === IMPORTANT : inventaire en dictionnaire ===
        # clé : nom de l'objet (str)
        # valeur : instance de Item
        # C'est ce que toute la logique du jeu utilise désormais.
        self.inventory = {}

        self.max_weight = 10

        # === NOUVEAU ===
        # Récompenses débloquées par les quêtes
        # (utilisé dans la commande "rewards")
        self.rewards = []

        # === NOUVEAU : état du beamer ===
        # Si le joueur possède un beamer, il peut "charger" une salle dedans.
        # beamer_room contient la Room mémorisée (ou None si rien n'est chargé).
        self.beamer_room = None

    # ------------------------------------------------------
    # Déplacement du joueur
    # ------------------------------------------------------
    def move(self, direction):
        direct = {'N', 'S', 'O', 'E', 'U', 'D'}
        
        # Vérifie que la direction existe
        if direction not in direct:
            print("\nDirection inconnue.\n")
            return False
        
        # Vérifie qu'on ne se déplace pas dans le vide
        next_room = self.current_room.exits[direction]

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Ajoute la pièce actuelle à l'historique AVANT d'aller dans la suivante
        self.history.append(self.current_room)

        # Effectue le déplacement
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    # ------------------------------------------------------
    # Historique des pièces visitées
    # ------------------------------------------------------
    def get_history(self):
        if not self.history:
            return ""
        lines = ["Vous avez déjà visité les pièces suivantes:"]
        for r in self.history:
            lines.append(f"    - {r.name}")  # plus propre que description
        return "\n" + "\n".join(lines) + "\n"

    # ------------------------------------------------------
    # Inventaire lisible
    # ------------------------------------------------------
    def get_inventory(self):
        if not self.inventory:
            return ""
        lines = ["Vous disposez des items suivants :"]
        for item in self.inventory.values():
            lines.append(f"    - {item.name} : {item.description}")
        return "\n" + "\n".join(lines) + "\n"
