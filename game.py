# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest, QuestObjective, QuestManager


class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.quest_manager = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        self.commands["history"] = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["back"]    = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["check"] = Command("check", " : afficher l'inventaire", Actions.check, 0)
        self.commands["look"] = Command("look", " : affiche les items dans la room", Actions.look, 0)
        self.commands["take"] = Command("take", " : ramasse un objet dans la salle", Actions.take, 1)
        self.commands["drop"] = Command("drop", " : dépose un objet dans la salle", Actions.drop, 1)
       
        self.commands["talk"] = Command(
            "talk",
            " <nom_pnj> : parler à un personnage présent dans la pièce",
            Actions.talk,
            1
        )

        self.commands["quests"] = Command(
            "quests",
            " : lister toutes les quêtes connues",
            Actions.quests,
            0
        )

        self.commands["quest"] = Command(
            "quest",
            " <nom_ou_id> : afficher le détail d'une quête",
            Actions.quest,
            1
        )

        self.commands["rewards"] = Command(
            "rewards",
            " : afficher les récompenses obtenues",
            Actions.rewards,
            0
        )

        # === NOUVEAU : commandes liées au beamer ===
        # charge : mémorise la salle actuelle dans le beamer (s'il est dans l'inventaire)
        self.commands["charge"] = Command(
            "charge",
            " : charge le beamer avec la pièce actuelle (si vous en avez un)",
            Actions.charge,
            0
        )

        # teleport : téléporte le joueur vers la salle mémorisée par le beamer
        self.commands["teleport"] = Command(
            "teleport",
            " : se téléporte vers la pièce mémorisée dans le beamer",
            Actions.teleport,
            0
        )

        # Setup rooms

        village = Room(
            "Village de Brumeval",
            "dans le petit village de Brumeval, presque désert. "
            "Les maisons sont fermées et une fontaine asséchée trône au centre."
        )
        self.rooms.append(village)

        ferme = Room(
            "Ferme abandonnée",
            "dans une ferme abandonnée. Des outils rouillés jonchent le sol "
            "et le vent fait claquer une porte."
        )
        self.rooms.append(ferme)

        foret = Room(
            "Forêt de Brume",
            "au cœur d'une forêt noyée dans une brume étrange. "
            "Les arbres semblent murmurer quelque chose d'inquiétant."
        )
        self.rooms.append(foret)

        lisiere_est = Room(
            "Lisière Est",
            "à la lisière est de la forêt, où les fougères rabougries "
            "témoignent de la Corruption."
        )
        self.rooms.append(lisiere_est)

        lisiere_ouest = Room(
            "Lisière Ouest",
            "à la lisière ouest de la forêt. Des insectes morts tapissent le sol."
        )
        self.rooms.append(lisiere_ouest)

        clairiere = Room(
            "Clairière corrompue",
            "dans une clairière dominée par un immense arbre noirci, "
            "cœur battant de la Corruption."
        )
        self.rooms.append(clairiere)

        sanctuaire = Room(
            "Sanctuaire ancien",
            "dans un vieux sanctuaire de pierre couvert de mousse. "
            "Des symboles gravés racontent une histoire oubliée."
        )
        self.rooms.append(sanctuaire)

        tombeau = Room(
            "Tombeau souterrain",
            "dans un tombeau souterrain humide, éclairé par une faible lueur verte. "
            "Un autel brisé se dresse au centre."
        )
        self.rooms.append(tombeau)

        # -----------------------------
        # 3) Création des sorties (exits)
        # -----------------------------


        village.exits = {"N": foret, "E": None,       "S": ferme,    "O": None,       "U": None,     "D": None}
        ferme.exits   = {"N": village, "E": None,     "S": None,     "O": None,       "U": None,     "D": None}
        foret.exits   = {"N": clairiere, "E": lisiere_est, "S": village, "O": lisiere_ouest, "U": None, "D": None}
        lisiere_est.exits = {"N": None, "E": None,    "S": None,     "O": foret,      "U": None,     "D": None}
        lisiere_ouest.exits = {"N": None, "E": foret, "S": None,     "O": None,       "U": None,     "D": None}
        clairiere.exits = {"N": sanctuaire, "E": None, "S": foret,   "O": None,       "U": None,     "D": None}
        sanctuaire.exits = {"N": None, "E": None,     "S": clairiere,"O": None,       "U": None,     "D": tombeau}
        tombeau.exits = {"N": None, "E": None,        "S": None,     "O": None,       "U": sanctuaire, "D": None}

        # -----------------------------
        # 4) Items (objets importants du scénario)
        # -----------------------------

        pierre_purete = Item(
            "pierre_purete",
            "une petite pierre claire et chaude au toucher, capable de dévoiler la Corruption.",
            1
        )

        graine_sacree = Item(
            "graine_sacree",
            "une graine lumineuse qui semble battre comme un cœur.",
            5
        )

        fragment_lame = Item(
            "fragment_lame",
            "un fragment de lame ancienne, ébréchée mais chargée de magie.",
            2
        )

        beamer = Item(
            "beamer",
            "un artefact ancien capable de mémoriser un lieu et de vous y ramener.",
            5
        )

        # On place les objets dans les inventaires des salles.
        # On ne remplace PAS inventory, on ajoute des entrées dans le dict existant.
        village.inventory[pierre_purete.name] = pierre_purete
        lisiere_est.inventory[graine_sacree.name] = graine_sacree
        ferme.inventory[fragment_lame.name] = fragment_lame
        sanctuaire.inventory[beamer.name] = beamer

        # -------------------------------------------------
        # 5) Characters (PNJ)
        # -------------------------------------------------
        # ⚠️ Même correction que pour inventory :
        # on considère Room.characters comme un dictionnaire nom -> Character.
        # C'est plus pratique pour accéder à un PNJ par son nom dans Actions.talk().

        herboriste = Character(
            "herboriste",
            "une vieille herboriste qui connaît les secrets de la forêt.",
            village,
            [
                "La forêt est malade... quelque chose a corrompu l'Arbre-Source.",
                "Si tu trouves une pierre de pureté, elle pourra t'aider à voir la Corruption."
            ]
        )

        forgeron = Character(
            "forgeron",
            "un forgeron exilé qui pourrait reforger une lame ancienne.",
            lisiere_ouest,
            [
                "Avec le bon métal, je peux recréer une lame purificatrice.",
                "Apporte-moi un fragment de lame, et je verrai ce que je peux faire."
            ]
        )

        esprit_foret = Character(
            "esprit",
            "un esprit affaibli, gardien du Sanctuaire.",
            sanctuaire,
            [
                "Je sens la Corruption monter des profondeurs du tombeau...",
                "Seule la graine sacrée et une lame purificatrice pourront sceller la faille.",
                "Lorsque tu seras prêt, descends dans le tombeau... mais pas sans ta lame purificatrice."
            ]
        )


        # Placement des PNJ dans les salles
        village.characters[herboriste.name] = herboriste
        lisiere_ouest.characters[forgeron.name] = forgeron
        sanctuaire.characters[esprit_foret.name] = esprit_foret

        # -------------------------------------------------
        # 6) Setup player and starting room
        # -------------------------------------------------

        self.player = Player(input("\nEntrez votre nom: "))

        # On commence logiquement dans le village
        self.player.current_room = village

         # -------------------------------------------------
        # -------------------------------------------------
        # 7) Quêtes : initialisation du QuestManager et 3 quêtes
        # -------------------------------------------------
        self.quest_manager = QuestManager()

        # =====================
        # Quête 1 : Comprendre la Corruption
        # =====================
        #
        # Objectifs :
        #  1) Parler à l'herboriste au village
        #  2) Ramasser la pierre de pureté
        #  3) Explorer la Forêt de Brume

        obj1_q1 = QuestObjective(
            "q1_obj1",
            "Parler à l'herboriste au village.",
            trigger_type="talk",
            trigger_value="herboriste"   # nom en minuscule (Actions.talk)
        )

        obj2_q1 = QuestObjective(
            "q1_obj2",
            "Ramasser la pierre de pureté.",
            trigger_type="take",
            trigger_value="pierre_purete"  # nom exact de l'item
        )

        obj3_q1 = QuestObjective(
            "q1_obj3",
            "Explorer la Forêt de Brume.",
            trigger_type="go",
            trigger_value="Forêt de Brume"  # Room.name exact
        )

        quest1 = Quest(
            "q1",
            "Comprendre la Corruption",
            "L'herboriste soupçonne qu'une force obscure corrompt la forêt. "
            "Parle-lui, récupère une pierre de pureté et va inspecter la Forêt de Brume.",
            [obj1_q1, obj2_q1, obj3_q1],
            "Tu as compris les premières causes de la Corruption de Brumeval."
        )

        self.quest_manager.add_quest(quest1)

        # =====================
        # Quête 2 : Reforger la lame
        # =====================
        #
        # Objectifs :
        #  1) Récupérer le fragment de lame à la ferme
        #  2) Parler au forgeron à la lisière ouest

        obj1_q2 = QuestObjective(
            "q2_obj1",
            "Récupérer le fragment de lame à la ferme abandonnée.",
            trigger_type="take",
            trigger_value="fragment_lame"
        )

        obj2_q2 = QuestObjective(
            "q2_obj2",
            "Parler au forgeron à la lisière ouest.",
            trigger_type="talk",
            trigger_value="forgeron"
        )

        quest2 = Quest(
            "q2",
            "Reforger la lame",
            "Un ancien fragment d'arme pourrait être reforgé. "
            "Récupère le fragment de lame et demande l'aide du forgeron.",
            [obj1_q2, obj2_q2],
            "Le forgeron accepte de reforger une lame purificatrice pour t'aider."
        )

        self.quest_manager.add_quest(quest2)

        # =====================
        # Quête 3 : Purifier le Cœur de la Forêt (quête finale)
        # =====================
        #
        # Objectifs :
        #  1) Ramasser la graine sacrée
        #  2) Parler à l'esprit au sanctuaire
        #  3) Se rendre dans la Clairière corrompue
        #  4) Descendre dans le Tombeau souterrain

        obj1_q3 = QuestObjective(
            "q3_obj1",
            "Ramasser la graine sacrée à la lisière est.",
            trigger_type="take",
            trigger_value="graine_sacree"
        )

        obj2_q3 = QuestObjective(
            "q3_obj2",
            "Parler à l'esprit au sanctuaire ancien.",
            trigger_type="talk",
            trigger_value="esprit"
        )

        obj3_q3 = QuestObjective(
            "q3_obj3",
            "Se rendre dans la Clairière corrompue.",
            trigger_type="go",
            trigger_value="Clairière corrompue"
        )

        obj4_q3 = QuestObjective(
            "q3_obj4",
            "Descendre dans le Tombeau souterrain.",
            trigger_type="go",
            trigger_value="Tombeau souterrain"
        )

        quest3 = Quest(
            "q3",
            "Purifier le Cœur de la Forêt",
            "Grâce à la graine sacrée et à la lame purificatrice forgée par le forgeron, "
            "tu peux purifier la source de la Corruption. Collecte la graine, consulte l'esprit, "
            "pénètre la clairière, puis descends dans le tombeau pour sceller la faille.",
            [obj1_q3, obj2_q3, obj3_q3, obj4_q3],
            "Tu as purifié le cœur de la forêt et sauvé Brumeval."
        )


        self.quest_manager.add_quest(quest3)


        # Si ton Player gère un historique (list des rooms déjà visitées),
        # tu peux éventuellement initialiser ici, par exemple :
        # self.player.history.append(village)
        # (à adapter à ton implémentation réelle de Player)

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split()

        # === PETITE SÉCURITÉ ===
        # Si le joueur appuie juste sur Entrée sans rien écrire,
        # list_of_words est vide et list_of_words[0] planterait.
        if not list_of_words:
            return

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure à Brumeval !")
        print("La forêt est corrompue... À toi de découvrir ce qui se cache derrière ce mal.")
        print("Entrez 'help' si vous avez besoin d'aide.\n")
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
