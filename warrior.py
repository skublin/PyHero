import pygame
from random import randint


IMAGES = {f'{f}-{n}-{d}': pygame.image.load(f'graphics/warriors/{f}/{n}/{d}.png')
          for f in ['demon', 'elf', 'human', 'undead']
          for n in range(1, 8)
          for d in ['left', 'right']}


class Warrior:
    """
    This class makes warriors and calculates damage.
    """
    def __init__(self, name, health, attack, defence, cost, nickname='Unknown'):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.cost = cost
        self.nickname = nickname
        self.actual_health = health
        self.image_left = IMAGES[f'{self.name}-left']
        self.image_right = IMAGES[f'{self.name}-right']
        self.owner = None
        self.done_attack = False

    def attack_points(self):
        warrior = (self.attack + self.randomness()) * (1 + self.owner.army[self] / 10)
        character = (self.owner.skills['Strength'] + self.owner.skills['Intellect']) / 5
        return round(warrior + character)

    def defence_points(self):
        warrior = (self.defence + self.randomness()) * (1 + self.owner.army[self] / 10)
        character = (self.owner.skills['Stamina'] + self.owner.skills['Agility'])
        return round(warrior + character)

    def damage_taken(self, target):
        # calculation of damage taken to target warrior by character's warrior
        damage = self.attack_points() - target.defence_points()
        if damage > 0:
            return damage
        else:
            return 0

    def randomness(self):
        # dice roll plus rounded character's Fortune skill value (divided by 5)
        return randint(1, 6) + round(self.owner.skills['Fortune'] / 5)
