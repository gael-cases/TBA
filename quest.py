# quest.py
# Système simple de quêtes réutilisable

class QuestObjective:
    """
    Un objectif de quête.
    - id : identifiant interne (q1_obj1, etc.)
    - description : texte affiché au joueur
    - trigger_type : "talk", "take", "go", ...
    - trigger_value : valeur associée ("herboriste", "pierre_purete", "Forêt de Brume", etc.)
    """

    def __init__(self, obj_id, description, trigger_type, trigger_value):
        self.id = obj_id
        self.description = description
        self.trigger_type = trigger_type
        self.trigger_value = trigger_value
        self.completed = False

    def try_complete(self, event_type, event_value):
        """
        Si l'événement correspond à cet objectif, on le marque comme complété.
        Retourne True si on vient de le compléter, False sinon.
        """
        if self.completed:
            return False

        if event_type == self.trigger_type and event_value == self.trigger_value:
            self.completed = True
            return True

        return False


class Quest:
    """
    Une quête composée de plusieurs objectifs.
    """

    def __init__(self, quest_id, name, description, objectives, reward_text):
        self.id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives  # liste de QuestObjective
        self.reward_text = reward_text

        # La quête est active dès le début
        self.active = True
        self.completed = False

    def notify(self, event_type, event_value, game):
        """
        Appelée par le QuestManager à chaque événement important.
        Parcourt les objectifs et tente de les compléter.
        Si tous les objectifs sont complétés → la quête est terminée.
        """
        if not self.active or self.completed:
            return

        changed = False
        for obj in self.objectives:
            if obj.try_complete(event_type, event_value):
                changed = True
                print(f"\n[Quête] Objectif complété : {obj.description}\n")

        # Si au moins un objectif a changé, on vérifie si la quête est finie
        if changed and self._all_objectives_completed():
            self.completed = True
            print(f"\n[Quête] Quête terminée : {self.name} !\n")
            self.give_reward(game)

    def _all_objectives_completed(self):
        return all(obj.completed for obj in self.objectives)

    def give_reward(self, game):
        """
        Ajoute un texte de récompense dans player.rewards
        + gère des récompenses spéciales selon la quête (objet, victoire, etc.).
        """
        player = game.player
        if not hasattr(player, "rewards"):
            player.rewards = []

        player.rewards.append(self.reward_text)
        print(f"[Récompense] {self.reward_text}\n")

        # === NOUVEAU : récompense spéciale pour la quête 2 ===
        if self.id == "q2":
            # On donne une vraie Lame purificatrice au joueur
            from item import Item
            lame = Item(
                "lame_purificatrice",
                "une lame reforgée par le forgeron, capable de canaliser la pureté.",
                3
            )
            player.inventory[lame.name] = lame
            print("[Objet] Vous recevez la Lame purificatrice du forgeron.\n")

        # Victoire pour la quête finale (q3)
        if self.id == "q3":
            # Import local pour éviter les imports circulaires
            import win
            win.game_won(game)


    def get_summary(self):
        """
        Retourne une ligne de résumé pour la commande 'quests'.
        """
        status = "terminée" if self.completed else "en cours" if self.active else "inactive"
        done = sum(1 for o in self.objectives if o.completed)
        total = len(self.objectives)
        return f"- {self.id} : {self.name} [{status}] ({done}/{total} objectifs)"

    def get_details(self):
        """
        Retourne une description détaillée pour la commande 'quest <id>'.
        """
        lines = [
            f"Quête {self.id} : {self.name}",
            "",
            self.description,
            "",
            "Objectifs :"
        ]
        for obj in self.objectives:
            mark = "✔" if obj.completed else "✘"
            lines.append(f"  {mark} {obj.description}")
        lines.append("")
        lines.append(f"Récompense : {self.reward_text}")
        return "\n".join(lines)


class QuestManager:
    """
    Gère plusieurs quêtes.
    """

    def __init__(self):
        self.quests = {}  # id -> Quest

    def add_quest(self, quest):
        self.quests[quest.id] = quest

    def notify(self, event_type, event_value, game):
        """
        Appelé par les Actions (take, drop, go, talk...).
        """
        for quest in self.quests.values():
            quest.notify(event_type, event_value, game)

    def get_quests_summary(self):
        """
        Utilisée par la commande 'quests'.
        """
        if not self.quests:
            return ""
        lines = ["Quêtes connues :"]
        for q in self.quests.values():
            lines.append(q.get_summary())
        return "\n" + "\n".join(lines) + "\n"

    def get_quest_details(self, quest_id):
        """
        Utilisée par la commande 'quest <id>'.
        On cherche par id exact ou par nom.
        """
        # D'abord par identifiant exact
        if quest_id in self.quests:
            return self.quests[quest_id].get_details()

        # Sinon, on essaie de comparer par nom (insensible à la casse)
        lowered = quest_id.lower()
        for q in self.quests.values():
            if q.name.lower() == lowered:
                return q.get_details()

        return ""
