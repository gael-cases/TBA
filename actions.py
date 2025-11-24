# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"


class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O, U, D).
        """
        player = game.player
        l = len(list_of_words)

        if l != number_of_parameters + 1:
            print("\nTu vas où ?\n")
            return False

        direction = list_of_words[1]

        # === NOUVEAU : vérification spéciale pour l'accès au Tombeau ===
        # Si le joueur est dans le Sanctuaire ancien, qu'il veut DESCENDRE (D),
        # mais qu'il n'a pas la lame_purificatrice, on bloque.
        current_room = player.current_room
        if (
            current_room.name == "Sanctuaire ancien"
            and direction == "D"
            and "lame_purificatrice" not in player.inventory
        ):
            print(
                "\nUne force invisible vous repousse au bord des marches.\n"
                "L'esprit du sanctuaire murmure : 'Tu ne peux affronter le tombeau "
                "sans la Lame purificatrice... Retourne voir le forgeron.'\n"
            )
            return False

        # Déplacement normal
        moved = player.move(direction)

        # Si le déplacement a réussi, on notifie les quêtes
        if moved and game.quest_manager is not None:
            try:
                current_room_name = player.current_room.name
                game.quest_manager.notify("go", current_room_name, game)
            except AttributeError:
                pass

        return moved



    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.
        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des pièces visitées.
        On délègue au Player via get_history().
        """
        txt = game.player.get_history()
        print(txt if txt else "\nAucun déplacement enregistré pour l'instant.\n")
        return False  # ne termine pas le tour

    def back(game, list_of_words, number_of_parameters):
        """
        Revient à la pièce précédente en utilisant la pile history du Player.
        """
        if not game.player.history:
            print("\nImpossible de revenir en arrière (aucun déplacement précédent).\n")
            return False

        prev_room = game.player.history.pop()
        game.player.current_room = prev_room
        print(game.player.current_room.get_long_description())
        print(game.player.get_history())
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur (via Player.get_inventory()).
        """
        txt = game.player.get_inventory()
        print(txt if txt else "\nVotre inventaire est vide.\n")
        return False

    def look(game, list_of_words, number_of_parameters):
        """
        Affiche le contenu de la salle courante :
        - description des objets
        - PNJ présents
        """
        current_room = game.player.current_room

        # On suppose que Room.get_inventory() renvoie une description textuelle
        print(current_room.get_inventory())

        # === ⚠️ CHANGEMENT : characters est un dict {nom: Character}
        if current_room.characters:
            print("Ici se trouve :\n")
            for char in current_room.characters.values():
                # char est un objet Character, on affiche son nom (ou str(char) si __str__ défini)
                print(f"    - {char.name}")
            print()
        return False

    def take(game, list_of_words, number_of_parameters):
        """
        Ramasse un objet dans la salle courante si :
        - il existe dans l'inventaire de la salle
        - le poids total n'excède pas max_weight du joueur

        ⚠️ CHANGEMENT IMPORTANT :
        On considère maintenant que les inventaires (joueur + salles) sont
        des dictionnaires {nom_item: Item} comme dans le cours.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        room = player.current_room

        # Calcul du poids actuel de l'inventaire du joueur
        inventory_weight = 0
        for item in player.inventory.values():
            inventory_weight += item.weight

        # Nom de l'item demandé
        item_name = list_of_words[1]

        # === ⚠️ CHANGEMENT : room.inventory est un dict
        if item_name not in room.inventory:
            print("\nIl n'y a pas cet objet ici.\n")
            return False

        item = room.inventory[item_name]

        # Vérification du poids
        if (inventory_weight + item.weight) <= player.max_weight:
            # On ajoute à l'inventaire du joueur
            player.inventory[item_name] = item
            # On enlève de la salle
            del room.inventory[item_name]
            print("\nVous avez ramassé " + item.name + ".\n")

            # === NOUVEAU : point d'accroche pour les quêtes ===
            # Si un système de quêtes est en place, on peut le prévenir ici
            # (par exemple: game.quest_manager.notify("take", item_name))
            if game.quest_manager is not None:
                try:
                    game.quest_manager.notify("take", item_name, game)
                except AttributeError:
                    # Si QuestManager n'a pas encore cette méthode, on ignore.
                    pass

            return True
        else:
            print(
                "\nVous allez être trop lourd, vous ne pouvez pas ramasser cet objet.\n"
                f"Votre poids : {inventory_weight}. "
                f"Votre poids maximum : {player.max_weight}.\n"
            )
            return False

    def drop(game, list_of_words, number_of_parameters):
        """
        Dépose un objet de l'inventaire du joueur dans la salle courante.

        ⚠️ CHANGEMENT :
        Utilisation de dictionnaires pour les inventaires.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print("\ndrop quoi ?\n")
            return False
        
        player = game.player
        room = player.current_room
        item_name = list_of_words[1]

        # === ⚠️ CHANGEMENT : player.inventory est un dict {nom: Item}
        if item_name not in player.inventory:
            print("\nVous n'avez pas cet objet.\n")
            return False

        item = player.inventory[item_name]

        # On enlève du joueur, on ajoute à la salle
        del player.inventory[item_name]
        room.inventory[item_name] = item
        print("\nVous avez déposé " + item.name + ".\n")

        # Les quêtes peuvent éventuellement être notifiées ici aussi.
        if game.quest_manager is not None:
            try:
                game.quest_manager.notify("drop", item_name, game)
            except AttributeError:
                pass

        return True

    # ============================================================
    # === NOUVELLES ACTIONS : TALK / QUESTS / QUEST / REWARDS ====
    # ============================================================

    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un PNJ présent dans la salle.
        Syntaxe : talk <nom_pnj>

        On cherche le PNJ dans current_room.characters (dict {nom: Character})
        puis on affiche un de ses messages (via Character.get_msg()).
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print("\nParler à qui ? Utilisation : talk <nom_pnj>\n")
            return False

        current_room = game.player.current_room
        pnj_name = list_of_words[1].lower()  # on normalise en minuscule

        if not current_room.characters:
            print("\nIl n'y a personne à qui parler ici.\n")
            return False

        # Les clés de current_room.characters sont en minuscule dans game.py
        if pnj_name not in current_room.characters:
            print(f"\nIl n'y a pas de personnage nommé '{pnj_name}' ici.\n")
            return False

        pnj = current_room.characters[pnj_name]

        # On suppose que Character.get_msg() renvoie une phrase à afficher.
        try:
            message = pnj.get_msg()
        except AttributeError:
            # Si get_msg n'est pas implémenté, on affiche juste la description.
            message = pnj.description

        print(f"\n{pnj.name} vous dit :\n\"{message}\"\n")

        # Point d'accroche pour les quêtes : parler à un PNJ peut déclencher
        # ou avancer une quête.
        if game.quest_manager is not None:
            try:
                game.quest_manager.notify("talk", pnj_name, game)
            except AttributeError:
                pass

        return True

    def quests(game, list_of_words, number_of_parameters):
        """
        Affiche la liste des quêtes connues.
        Pour l'instant, cette action se contente de déléguer au QuestManager
        si il existe, sinon d'afficher un message explicite.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        if game.quest_manager is None:
            print("\nAucun système de quêtes n'est encore en place.\n")
            return False

        # On suppose que quest_manager.get_quests_summary() renvoie une chaîne.
        try:
            txt = game.quest_manager.get_quests_summary()
        except AttributeError:
            print("\nLe gestionnaire de quêtes ne fournit pas encore de résumé.\n")
            return False

        print(txt if txt else "\nAucune quête connue pour l'instant.\n")
        return False

    def quest(game, list_of_words, number_of_parameters):
        """
        Affiche le détail d'une quête particulière.
        Syntaxe : quest <nom_ou_id>
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print("\nQuel(le) quête ? Utilisation : quest <nom_ou_id>\n")
            return False

        if game.quest_manager is None:
            print("\nAucun système de quêtes n'est encore en place.\n")
            return False

        quest_id = list_of_words[1]

        # On suppose que quest_manager.get_quest_details(id) renvoie une chaîne.
        try:
            txt = game.quest_manager.get_quest_details(quest_id)
        except AttributeError:
            print("\nLe gestionnaire de quêtes ne permet pas encore d'afficher "
                  "les détails d'une quête.\n")
            return False

        print(txt if txt else f"\nAucune quête trouvée avec l'identifiant '{quest_id}'.\n")
        return False

    def rewards(game, list_of_words, number_of_parameters):
        """
        Affiche les récompenses obtenues par le joueur.
        Pour l'instant, on vérifie simplement si le Player possède un attribut
        'rewards' (par exemple une liste ou un dict).
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        # Si l'attribut n'existe pas, on le crée vide pour éviter les crashes.
        if not hasattr(player, "rewards"):
            player.rewards = []

        if not player.rewards:
            print("\nVous n'avez obtenu aucune récompense pour le moment.\n")
            return False

        print("\nRécompenses obtenues :")
        for r in player.rewards:
            print(f"  - {r}")
        print()
        return False
    
        # ============================================================
    # === ACTIONS BEAMER : CHARGE & TELEPORT =====================
    # ============================================================

    def charge(game, list_of_words, number_of_parameters):
        """
        Charge le beamer avec la salle actuelle.
        Conditions :
        - le joueur doit posséder un objet nommé 'beamer' dans son inventaire
        - pas de paramètre
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        # Vérifier que le joueur a bien le beamer
        if "beamer" not in player.inventory:
            print("\nVous ne possédez pas de beamer.\n")
            return False

        # On mémorise la room actuelle dans le beamer
        player.beamer_room = player.current_room
        print(f"\nLe beamer est maintenant chargé avec : {player.current_room.name}.\n")
        return False  # on considère que ça ne consomme pas le tour

    def teleport(game, list_of_words, number_of_parameters):
        """
        Téléporte le joueur vers la salle mémorisée dans le beamer.
        Conditions :
        - le joueur doit avoir le beamer
        - le beamer doit avoir une salle mémorisée (charge déjà utilisé)
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        if "beamer" not in player.inventory:
            print("\nVous ne possédez pas de beamer.\n")
            return False

        if player.beamer_room is None:
            print("\nLe beamer n'est pas chargé. Utilisez d'abord la commande 'charge'.\n")
            return False

        # Téléportation
        player.current_room = player.beamer_room
        print("\nLe beamer scintille et vous sentez l'espace se plier...\n")
        print(player.current_room.get_long_description())

        # Option : on vide le beamer après usage si vous voulez qu'il soit one-shot :
        # player.beamer_room = None

        # On notifie éventuellement les quêtes que le joueur est arrivé dans cette pièce
        if game.quest_manager is not None:
            try:
                game.quest_manager.notify("go", player.current_room.name, game)
            except AttributeError:
                pass

        return True

