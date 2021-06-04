from warrior import *
from random import randint
import pygame


# list of possible warriors in every fraction Warrior(name, health, attack, defence, cost)
# it's a dictionary '[fraction name]': list(Warriors from class Warrior)
WARRIORS = {'Demon': [Warrior('Demon-1', 30, 10, 8, 5), Warrior('Demon-2', 30, 10, 8, 5),
                      Warrior('Demon-3', 30, 10, 8, 5), Warrior('Demon-4', 30, 10, 8, 5),
                      Warrior('Demon-5', 30, 10, 8, 5), Warrior('Demon-6', 30, 10, 8, 5),
                      Warrior('Demon-7', 30, 10, 8, 5)],
            'Elf': [Warrior('Elf-1', 30, 10, 8, 5), Warrior('Elf-2', 30, 10, 8, 5),
                    Warrior('Elf-3', 30, 10, 8, 5), Warrior('Elf-4', 30, 10, 8, 5),
                    Warrior('Elf-5', 30, 10, 8, 5), Warrior('Elf-6', 30, 10, 8, 5),
                    Warrior('Elf-7', 30, 10, 8, 5)],
            'Human': [Warrior('Human-1', 30, 10, 8, 5), Warrior('Human-2', 30, 10, 8, 5),
                      Warrior('Human-3', 30, 10, 8, 5), Warrior('Human-4', 30, 10, 8, 5),
                      Warrior('Human-5', 30, 10, 8, 5), Warrior('Human-6', 30, 10, 8, 5),
                      Warrior('Human-7', 30, 10, 8, 5)],
            'Undead': [Warrior('Undead-1', 30, 10, 8, 5), Warrior('Undead-2', 30, 10, 8, 5),
                       Warrior('Undead-3', 30, 10, 8, 5), Warrior('Undead-4', 30, 10, 8, 5),
                       Warrior('Undead-5', 30, 10, 8, 5), Warrior('Undead-6', 30, 10, 8, 5),
                       Warrior('Undead-7', 30, 10, 8, 5)]}


class Character:
    def __init__(self, game, name, color, fraction, position):
        self.game = game
        self.name = name
        self.color = color
        self.flag = pygame.image.load(f'graphics/flags/{self.color}_small.png')
        self.fraction = fraction
        self.level = 1
        self.experience = 0
        self.army = WARRIORS['Human']   # as a list or something else?
        self.position = position
        self.moves = 6

    def add_warrior(self):
        pass

    def remove_warrior(self):
        pass

    def find_road(self, start, end):
        self.game.dij.dijkstra(start)
        road = self.game.dij.traverse(end)
        move_cost = len(road) - 1
        return road, move_cost

    @staticmethod
    def matrix_position(x, y):
        i = (y - 138) // 55
        off_j = 44 if i % 2 == 0 else 76
        j = (x - off_j) // 64
        return i, j


class Player(Character):
    def __init__(self, game, name, color, fraction, position):
        super().__init__(game, name, color, fraction, position)
        self.money = 20

    def move(self, destination):
        x, y = destination
        i, j = self.matrix_position(x, y)
        road, move_cost = self.find_road(self.matrix_position(self.position[0], self.position[1]),
                                         (i, j))
        self.game.prompt = True
        while self.moves < move_cost:
            if self.moves == 0:
                self.game.open_prompt('You have no moves!', 'Do you want to start next turn now?')
                if self.game.prompt_answer:
                    if self.game.answer == 'yes':
                        self.game.new_turn = True
                        break
                    else:
                        break
            else:
                self.game.open_prompt(f'Not enough moves ({move_cost})!', f'Do you want to go in this direction?')
                if self.game.prompt_answer:
                    if self.game.answer == 'yes':
                        road = road[:self.moves + 1]
                        self.moves = 0
                        break
                    else:
                        break
        while self.moves >= move_cost:
            self.game.open_prompt('Are you sure?', f"It cost {move_cost} moves!")
            if self.game.prompt_answer:
                if self.game.answer == 'yes':
                    self.moves -= move_cost
                    break
                else:
                    break
        self.game.prompt_answer, self.game.prompt = False, False
        return road


class Enemy(Character):
    def __init__(self, game, name, color, fraction, position, difficulty=1):
        super().__init__(game, name, color, fraction, position)
        self.difficulty = difficulty

    def make_move(self):
        i, j = randint(0, 12), randint(0, 14)
        road, move_cost = self.find_road(self.matrix_position(self.position[0], self.position[1]),
                                         (i, j))
        if self.moves < move_cost:
            road = road[:self.moves + 1]
            self.moves = 0
        elif self.moves >= move_cost:
            self.moves -= move_cost
        return road

    def difficulty_change(self):
        return self.difficulty
