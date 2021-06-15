from warrior import *
from random import randint
import pygame


# list of possible warriors in every fraction Warrior(name, health, attack, defence, cost)
# it's a dictionary '[fraction name]': list(Warriors from class Warrior)
WARRIORS = {'Demon': [Warrior('demon-1', 30, 10, 8, 5), Warrior('demon-2', 30, 10, 8, 5),
                      Warrior('demon-3', 30, 10, 8, 5), Warrior('demon-4', 30, 10, 8, 5),
                      Warrior('demon-5', 30, 10, 8, 5), Warrior('demon-6', 30, 10, 8, 5),
                      Warrior('demon-7', 30, 10, 8, 5)],
            'Elf': [Warrior('elf-1', 30, 10, 8, 5), Warrior('elf-2', 30, 10, 8, 5),
                    Warrior('elf-3', 30, 10, 8, 5), Warrior('elf-4', 30, 10, 8, 5),
                    Warrior('elf-5', 30, 10, 8, 5), Warrior('elf-6', 30, 10, 8, 5),
                    Warrior('elf-7', 30, 10, 8, 5)],
            'Human': [Warrior('human-1', 30, 10, 8, 5), Warrior('human-2', 30, 10, 8, 5),
                      Warrior('human-3', 30, 10, 8, 5), Warrior('human-4', 30, 10, 8, 5),
                      Warrior('human-5', 30, 10, 8, 5), Warrior('human-6', 30, 10, 8, 5),
                      Warrior('human-7', 30, 10, 8, 5)],
            'Undead': [Warrior('undead-1', 30, 10, 8, 5), Warrior('undead-2', 30, 10, 8, 5),
                       Warrior('undead-3', 30, 10, 8, 5), Warrior('undead-4', 30, 10, 8, 5),
                       Warrior('undead-5', 30, 10, 8, 5), Warrior('undead-6', 30, 10, 8, 5),
                       Warrior('undead-7', 30, 10, 8, 5)]}


IMAGES = {'button_plus': pygame.image.load('graphics/btn/button_plus.png'),
          'button_minus': pygame.image.load('graphics/btn/button_minus.png')}


class Character:
    def __init__(self, game, name, color, fraction, position):
        self.game = game
        self.name = name
        self.color = color
        self.fraction = fraction
        self.position = position
        self.flag = pygame.image.load(f'graphics/flags/{self.color}_small.png')
        self.level = 1
        self.experience = 0
        self.skill_points = 10
        self.skills = {'Strength': 5, 'Stamina': 5, 'Wisdom': 5, 'Intellect': 5, 'Agility': 5, 'Charm': 5, 'Fortune': 5}
        self.army = {warrior: 0 for warrior in WARRIORS[self.fraction]}
        self.money = 100
        self.moves = 6

    def add_warrior(self, number, amount):
        """
        This method lets characters buy new warriors to army (if enough money).
        """
        if self.money >= WARRIORS[f'{self.fraction}'][number - 1].cost * amount:
            self.army[f'{self.fraction.lower()}-{number}'] += amount
            self.money -= WARRIORS[f'{self.fraction}'][number - 1].cost * amount
        else:
            return False

    def remove_warrior(self, number, amount):
        """
        This method lets characters sell warriors from army and have 50% money back.
        """
        if self.army[f'{self.fraction.lower()}-{number}'] >= amount:
            self.army[f'{self.fraction.lower()}-{number}'] -= amount
            self.money += (WARRIORS[f'{self.fraction}'][number - 1].cost * amount) / 2
        else:
            return False

    def find_road(self, start, end):
        """
        With prepared graph for Dijkstra algorithm and given points of start and end this method calculates best road.
        """
        self.game.dij.dijkstra(start)
        road = self.game.dij.traverse(end)
        move_cost = len(road) - 1
        return road, move_cost

    @staticmethod
    def matrix_position(x, y):
        """
        Side method just to transform x, y coordinates to i, j position on the map (also graph) represented as matrix.
        """
        i = (y - 138) // 55
        off_j = 44 if i % 2 == 0 else 76
        j = (x - off_j) // 64
        return i, j


class Player(Character):
    """
    Subclass of Character for specific methods used by person playing this game.
    """
    def __init__(self, game, name, color, fraction, position):
        super().__init__(game, name, color, fraction, position)
        self.skill_buttons = dict()

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

    def character_info(self, image):
        while self.game.character_prompt:
            self.game.check_events()
            # PROBABLY IT'S FINE TO REMOVE if AND elif STATEMENTS
            if self.game.ESCAPE_KEY:
                self.game.character_prompt = False
            elif self.game.START_KEY:
                self.game.character_prompt = False
            self.game.draw_interface()
            self.game.display.blit(image, (204, 256))
            skills_names = ['Strength', 'Stamina', 'Wisdom', 'Intellect', 'Agility', 'Charm', 'Fortune']
            # LEFT SIDE OF PROMPT WINDOW
            self.game.draw_text('Character:', 36, 380, 302, text_format='c')
            self.game.draw_text(f'{self.name}', 34, 380, 350, text_format='c')
            self.game.draw_text(f'Fraction: {self.fraction}', 32, 380, 390, text_format='c')
            self.game.draw_text(f'Level: {self.level}', 32, 380, 430, text_format='c')
            self.game.draw_text(f'XP: {self.experience} / 100', 32, 380, 470, text_format='c')
            self.game.draw_text(f'Money: {self.money}', 32, 380, 510, text_format='c')
            self.game.draw_text(f'Battles: {self.game.battle_number}', 32, 380, 550, text_format='c')
            # RIGHT SIDE OF PROMPT WINDOW
            self.game.draw_text('Skills:', 36, 672, 302, text_format='c')
            self.game.draw_text(f'Points: {self.skill_points}', 34, 536, 329, text_format='tl')
            for i in range(7):
                self.game.draw_text(f"{skills_names[i]}: {self.skills[skills_names[i]]}",
                                    32, 536, 370 + i * 40, text_format='tl')
                self.skill_buttons[f'{skills_names[i]}_minus'] = self.game.display.blit(IMAGES['button_minus'],
                                                                                        (730, 370 + i * 40))
                self.skill_buttons[f'{skills_names[i]}_plus'] = self.game.display.blit(IMAGES['button_plus'],
                                                                                       (772, 370 + i * 40))
            # BLIT AND UPDATE
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()

    def skill_change(self, button_clicked):
        skill, symbol = button_clicked.split('_')
        if symbol == 'plus' and self.skill_points > 0:
            self.skills[skill] += 1
            self.skill_points -= 1
        elif symbol == 'minus' and self.skills[skill] > 5:
            self.skills[skill] -= 1
            self.skill_points += 1


class Enemy(Character):
    """
    Subclass of Character to control enemy.
    """
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

    # not implemented yet
    def difficulty_change(self):
        return self.difficulty
