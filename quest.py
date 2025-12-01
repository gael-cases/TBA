# quest.py
class QuestObjective:

    def __init__(self, obj_id, description, trigger_type, trigger_value):
        self.id = obj_id
        self.description = description
        self.trigger_type = trigger_type
        self.trigger_value = trigger_value
        self.completed = False

    def try_complete(self, event_type, event_value):
        if self.completed:
            return False

        if event_type == self.trigger_type and event_value == self.trigger_value:
            self.completed = True
            return True

        return False


class Quest:

    def __init__(self, quest_id, name, description, objectives, reward_text):
        self.id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives
        self.reward_text = reward_text

        self.active = True
        self.completed = False

    def notify(self, event_type, event_value, game):
        if not self.active or self.completed:
            return

        changed = False
        for obj in self.objectives:
            if obj.try_complete(event_type, event_value):
                changed = True
                print(f"\n[Quête] Objectif complété : {obj.description}\n")

        if changed and self._all_objectives_completed():
            self.completed = True
            print(f"\n[Quête] Quête terminée : {self.name} !\n")
            self.give_reward(game)

    def _all_objectives_completed(self):
        return all(obj.completed for obj in self.objectives)

    def give_reward(self, game):
        player = game.player
        if not hasattr(player, "rewards"):
            player.rewards = []

        player.rewards.append(self.reward_text)
        print(f"[Récompense] {self.reward_text}\n")

        if self.id == "q2":
            from item import Item
            lame = Item(
                "lame_purificatrice",
                "une lame reforgée par le forgeron, capable de canaliser la pureté.",
                3
            )
            player.inventory[lame.name] = lame
            print("[Objet] Vous recevez la Lame purificatrice du forgeron.\n")

        if self.id == "q3":
            import win
            win.game_won(game)

    def get_summary(self):
        status = "terminée" if self.completed else "en cours" if self.active else "inactive"
        done = sum(1 for o in self.objectives if o.completed)
        total = len(self.objectives)
        return f"- {self.id} : {self.name} [{status}] ({done}/{total} objectifs)"

    def get_details(self):
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

    def __init__(self):
        self.quests = {}

    def add_quest(self, quest):
        self.quests[quest.id] = quest

    def notify(self, event_type, event_value, game):
        for quest in self.quests.values():
            quest.notify(event_type, event_value, game)

    def get_quests_summary(self):
        if not self.quests:
            return ""
        lines = ["Quêtes connues :"]
        for q in self.quests.values():
            lines.append(q.get_summary())
        return "\n" + "\n".join(lines) + "\n"

    def get_quest_details(self, quest_id):
        if quest_id in self.quests:
            return self.quests[quest_id].get_details()

        lowered = quest_id.lower()
        for q in self.quests.values():
            if q.name.lower() == lowered:
                return q.get_details()

        return ""