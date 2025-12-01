class Character():

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.msg_index = 0

    def __str__(self):
        return self.name + " : " + self.description

    def get_msg(self):
        if not self.msgs:
            return "… (ce personnage reste silencieux)"

        msg = self.msgs[self.msg_index]

        self.msg_index = (self.msg_index + 1) % len(self.msgs)

        return msg