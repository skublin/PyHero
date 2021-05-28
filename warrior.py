
IMAGES = {'name': 'loaded_image'}


class Warrior:
    def __init__(self, name, health, attack, defence, cost):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.cost = cost
        self.image = IMAGES[self.name]

    def attack(self):
        pass

    def defend(self):
        pass
