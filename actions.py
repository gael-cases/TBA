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
        player = game.player
        l = len(list_of_words)

        if l != number_of_parameters + 1:
            print("\nTu vas où ?\n")
            return False

        direction = list_of_words[1]

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

        moved = player.move(direction)

        if moved and game.quest_manager is not None:
            try:
                current_room_name = player.current_room.name
                game.quest_manager.notify("go", current_room_name, game)
            except AttributeError:
                pass

        return moved



    def quit(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
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
        txt = game.player.get_history()
        print(txt if txt else "\nAucun déplacement enregistré pour l'instant.\n")
        return False

    def back(game, list_of_words, number_of_parameters):
        if not game.player.history:
            print("\nImpossible de revenir en arrière (aucun déplacement précédent).\n")
            return False

        prev_room = game.player.history.pop()
        game.player.current_room = prev_room
        print(game.player.current_room.get_long_description())
        print(game.player.get_history())
        return True

    def check(game, list_of_words, number_of_parameters):
        txt = game.player.get_inventory()
        print(txt if txt else "\nVotre inventaire est vide.\n")
        return False

    def look(game, list_of_words, number_of_parameters):
        current_room = game.player.current_room

        print(current_room.get_inventory())

        if current_room.characters:
            print("Ici se trouve :\n")
            for char in current_room.characters.values():
                print(f"    - {char.name}")
            print()
        return False

    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        room = player.current_room

        inventory_weight = 0
        for item in player.inventory.values():
            inventory_weight += item.weight

        item_name = list_of_words[1]

        if item_name not in room.inventory:
            print("\nIl n'y a pas cet objet ici.\n")
            return False

        item = room.inventory[item_name]

        if (inventory_weight + item.weight) <= player.max_weight:
            player.inventory[item_name] = item
            del room.inventory[item_name]
            print("\nVous avez ramassé " + item.name + ".\n")

            if game.quest_manager is not None:
                try:
                    game.quest_manager.notify("take", item_name, game)
                except AttributeError:
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
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print("\ndrop quoi ?\n")
            return False
        
        player = game.player
        room = player.current_room
        item_name = list_of_words[1]

        if item_name not in player.inventory:
            print("\nVous n'avez pas cet objet.\n")
            return False

        item = player.inventory[item_name]

        del player.inventory[item_name]
        room.inventory[item_name] = item
        print("\nVous avez déposé " + item.name + ".\n")

        if game.quest_manager is not None:
            try:
                game.quest_manager.notify("drop", item_name, game)
            except AttributeError:
                pass

        return True

    def talk(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print("\nParler à qui ? Utilisation : talk <nom_pnj>\n")
            return False

        current_room = game.player.current_room
        pnj_name = list_of_words[1].lower()

        if not current_room.characters:
            print("\nIl n'y a personne à qui parler ici.\n")
            return False

        if pnj_name not in current_room.characters:
            print(f"\nIl n'y a pas de personnage nommé '{pnj_name}' ici.\n")
            return False

        pnj = current_room.characters[pnj_name]

        try:
            message = pnj.get_msg()
        except AttributeError:
            message = pnj.description

        print(f"\n{pnj.name} vous dit :\n\"{message}\"\n")

        if game.quest_manager is not None:
            try:
                game.quest_manager.notify("talk", pnj_name, game)
            except AttributeError:
                pass

        pnj.move()

        return True

    def quests(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        if game.quest_manager is None:
            print("\nAucun système de quêtes n'est encore en place.\n")
            return False

        try:
            txt = game.quest_manager.get_quests_summary()
        except AttributeError:
            print("\nLe gestionnaire de quêtes ne fournit pas encore de résumé.\n")
            return False

        print(txt if txt else "\nAucune quête connue pour l'instant.\n")
        return False

    def quest(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print("\nQuel(le) quête ? Utilisation : quest <nom_ou_id>\n")
            return False

        if game.quest_manager is None:
            print("\nAucun système de quêtes n'est encore en place.\n")
            return False

        quest_id = list_of_words[1]

        try:
            txt = game.quest_manager.get_quest_details(quest_id)
        except AttributeError:
            print("\nLe gestionnaire de quêtes ne permet pas encore d'afficher "
                  "les détails d'une quête.\n")
            return False

        print(txt if txt else f"\nAucune quête trouvée avec l'identifiant '{quest_id}'.\n")
        return False

    def rewards(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        if not hasattr(player, "rewards"):
            player.rewards = []

        if not player.rewards:
            print("\nVous n'avez obtenu aucune récompense pour le moment.\n")
            return False

        print("\nRécompenses obtenues :")
        for r in player.rewards:
            print(f"    - {r}")
        print()
        return False
    
    def charge(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player

        if "beamer" not in player.inventory:
            print("\nVous ne possédez pas de beamer.\n")
            return False

        player.beamer_room = player.current_room
        print(f"\nLe beamer est maintenant chargé avec : {player.current_room.name}.\n")
        return False

    def teleport(game, list_of_words, number_of_parameters):
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

        player.current_room = player.beamer_room
        print("\nLe beamer scintille et vous sentez l'espace se plier...\n")
        print(player.current_room.get_long_description())

        # player.beamer_room = None

        if game.quest_manager is not None:
            try:
                game.quest_manager.notify("go", player.current_room.name, game)
            except AttributeError:
                pass

        return True