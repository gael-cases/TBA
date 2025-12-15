import random


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
            return "…"
        msg = self.msgs[self.msg_index]
        self.msg_index = (self.msg_index + 1) % len(self.msgs)
        return msg

    
    def move(self):
        """
        À chaque tour :
        - 1 chance sur 2 de rester sur place
        - sinon, déplacement vers une pièce adjacente au hasard
        Retourne True si déplacement, False sinon
        """

        # 1 chance sur 2 de rester immobile
        if random.choice([True, False]) is False:
            return False 
     

        # Récupérer les sorties valides
        exits = [room for room in self.current_room.exits.values() if room is not None]

      

        # Choix aléatoire d'une pièce adjacente
        next_room = random.choice(exits)
        print(f"{self.name} est ici : {self.current_room.name}")

        # Retirer le PNJ de la pièce actuelle
        del self.current_room.characters[self.name]

        # Déplacement
        self.current_room = next_room
        next_room.characters[self.name] = self


        return True
