class Character():

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room

        # Liste de messages donnés quand on parle à ce PNJ
        self.msgs = msgs

        # === NOUVEAU ===
        # Index permettant de donner les messages en boucle
        self.msg_index = 0

    def __str__(self):
        return self.name + " : " + self.description

    # === NOUVEAU ===
    def get_msg(self):
        """
        Retourne le prochain message du PNJ.
        Les messages tournent en boucle.
        """
        if not self.msgs:
            return "… (ce personnage reste silencieux)"

        msg = self.msgs[self.msg_index]

        # Avance dans la liste des messages (mode boucle)
        self.msg_index = (self.msg_index + 1) % len(self.msgs)

        return msg
