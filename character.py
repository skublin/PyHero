import pygame
from warrior import *


# list of possible warriors in every fraction
# it's a dictionary '[fraction name]': list(Warriors from class Warrior)
ARMIES = {'Demon': [Warrior('0', 30, 10, 8, 5)], 'Elf': [], 'Human': [], 'Undead': []}


class Character:
    def __init__(self, game, name, color, fraction, position):
        self.game = game
        self.name = name
        self.color = color
        self.flag = pygame.image.load(f'graphics/flags/{self.color}_small.png')
        self.fraction = fraction
        self.level = 1
        self.experience = 0
        # self.army = [(warrior, 0) for warrior in ARMIES[self.fraction]]
        self.position = position
        self.moves = 10

    def add_warrior(self):
        pass

    def remove_warrior(self):
        pass


class Player(Character):
    def __init__(self, game, name, color, fraction, position):
        super().__init__(game, name, color, fraction, position)
        self.money = 0

    def dice_roll(self):
        pass

    def move(self):
        pass


class Enemy(Character):
    def __init__(self, game, name, color, fraction, position, difficulty=1):
        super().__init__(game, name, color, fraction, position)
        self.difficulty = difficulty

    def difficulty_change(self):
        pass

    def make_move(self):
        pass
