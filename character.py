from warrior import *
from random import randint, choice
import pygame


# list of possible warriors in every fraction Warrior(name, health, attack, defence, cost)
# it's a dictionary '[fraction name]': list(Warriors from class Warrior)
WARRIORS = {'Demon': [Warrior('demon-1', 20, 8, 8, 5, 'Devil'), Warrior('demon-2', 20, 14, 6, 10, 'Warlock'),
                      Warrior('demon-3', 25, 16, 12, 20, 'Flamer'), Warrior('demon-4', 30, 20, 12, 30, 'Nija'),
                      Warrior('demon-5', 50, 24, 12, 40, 'Mammon'), Warrior('demon-6', 50, 30, 20, 60, 'Tchort'),
                      Warrior('demon-7', 60, 32, 24, 80, 'Fenriz')],
            'Elf': [Warrior('elf-1', 20, 8, 8, 5, 'Aegnor'), Warrior('elf-2', 20, 14, 6, 10, 'Agada'),
                    Warrior('elf-3', 25, 16, 12, 20, 'Aveley'), Warrior('elf-4', 30, 20, 12, 30, 'Alfur'),
                    Warrior('elf-5', 50, 24, 12, 40, 'Alvgjerd'), Warrior('elf-6', 50, 30, 20, 60, 'Fangorn'),
                    Warrior('elf-7', 60, 32, 24, 80, 'Unicorn')],
            'Human': [Warrior('human-1', 20, 8, 8, 5, 'Merek'), Warrior('human-2', 20, 14, 6, 10, 'Rowan'),
                      Warrior('human-3', 25, 16, 12, 20, 'Fendrel'), Warrior('human-4', 30, 20, 12, 30, 'Emeline'),
                      Warrior('human-5', 50, 24, 12, 40, 'Althalos'), Warrior('human-6', 50, 30, 20, 60, 'Cassius'),
                      Warrior('human-7', 60, 32, 24, 80, 'Berinon')],
            'Undead': [Warrior('undead-1', 20, 8, 8, 5, 'Regis'), Warrior('undead-2', 20, 14, 6, 10, 'Jendrich'),
                       Warrior('undead-3', 25, 16, 12, 20, 'Dracula'), Warrior('undead-4', 30, 20, 12, 30, 'Mummy'),
                       Warrior('undead-5', 50, 24, 12, 40, 'Reaper'), Warrior('undead-6', 50, 30, 20, 60, 'Shana'),
                       Warrior('undead-7', 60, 32, 24, 80, 'Egidius')]}


IMAGES = {'warrior_info': pygame.image.load('graphics/btn/warrior_info.png'),
          'button_plus': pygame.image.load('graphics/btn/button_plus.png'),
          'button_minus': pygame.image.load('graphics/btn/button_minus.png'),
          'coin': pygame.image.load('graphics/coin.png'),
          'warrior_table': pygame.image.load('graphics/warrior_table.png'),
          'warrior_health': pygame.image.load('graphics/warrior_health.png'),
          'warrior_attack': pygame.image.load('graphics/warrior_attack.png'),
          'warrior_defence': pygame.image.load('graphics/warrior_defence.png')}


class Character:
    """
    This class creates basic hero, with attributes and methods for both Player and Enemy.
    """
    def __init__(self, game, name, color, fraction, position):
        self.game = game
        self.name = name
        self.color = color
        self.fraction = fraction
        self.position = position
        self.flag = pygame.image.load(f'graphics/flags/{self.color}_small.png')
        self.level = 1
        self.experience = 20
        self.to_level_up = 100
        self.skill_points = 10
        self.skills = {'Strength': 5, 'Stamina': 5, 'Wisdom': 5, 'Intellect': 5, 'Agility': 5, 'Charm': 5, 'Fortune': 5}
        self.army = dict()
        self.money = 200
        self.moves = 8

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

    def make_army(self):
        self.army = {warrior: 1 for warrior in WARRIORS[self.fraction]}
        for warrior, i in zip(self.army, range(1, 8)):
            warrior.owner = self
            if i == 1:
                self.army[warrior] = 20
            elif i == 2:
                self.army[warrior] = 16
            elif i == 3:
                self.army[warrior] = 12
            elif i == 4:
                self.army[warrior] = 8
            elif i == 5:
                self.army[warrior] = 4
            elif i == 6:
                self.army[warrior] = 2
            elif i == 7:
                self.army[warrior] = 1

    def warriors_alive(self, index):
        """
        Check warrior with index number if is alive (more than 0 warriors)
        """
        for warrior, i in zip(self.army, range(1, 8)):
            if i == index:
                if self.army[warrior] > 0:
                    return True
                else:
                    return False

    @staticmethod
    def alive_in_army(character):
        return [warrior for warrior in character.army if character.army[warrior] > 0]

    def check_level_up(self):
        if self.experience >= self.to_level_up:
            self.experience -= self.to_level_up
            self.level += 1
            self.skill_points += 10
            self.money += 100


class Player(Character):
    """
    Subclass of Character for specific methods used by person playing this game.
    """
    def __init__(self, game, name, color, fraction, position):
        super().__init__(game, name, color, fraction, position)
        self.skill_buttons = dict()
        self.army_shop_buttons = dict()
        self.open_info = False

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
            if self.game.ESCAPE_KEY:
                self.game.character_prompt = False
            self.game.draw_interface()
            self.game.display.blit(image, (204, 256))
            skills_names = ['Strength', 'Stamina', 'Wisdom', 'Intellect', 'Agility', 'Charm', 'Fortune']
            # LEFT SIDE OF PROMPT WINDOW
            self.game.draw_text('Character:', 36, 380, 302, text_format='c')
            self.game.draw_text(f'{self.name}', 34, 380, 350, text_format='c')
            self.game.draw_text(f'{self.fraction}', 32, 380, 390, text_format='c')
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

    def army_info(self, image):
        while self.game.army_prompt:
            self.game.check_events()
            if self.game.ESCAPE_KEY:
                self.game.army_prompt = False
            self.game.draw_interface()
            self.game.display.blit(image, (204, 256))
            # DRAW ARMY INFO, COST AND BUTTONS
            for warrior, i in zip(self.army, range(1, 8)):
                field = warrior.image_right.get_rect()
                offset = (i - 1) * 133 if i < 4 else (i - 5) * 133
                next_row = 0 if i < 4 else 164
                field.bottomleft = (403 + offset, 426 + next_row)
                self.game.draw_text(f'{self.army[warrior]}', 32, 459.5 + offset, 456 + next_row - next_row * 0.061, 'c')
                self.game.draw_text(f'{warrior.cost}', 32, 483 + offset, 426 + next_row, 'bl')
                self.game.display.blit(IMAGES['coin'], (483 + offset, 369 + next_row))
                self.army_shop_buttons[f'{warrior.name}_minus'] = self.game.display.blit(
                    IMAGES['button_minus'], (403 + offset, 438 + next_row - next_row * 0.061))
                self.army_shop_buttons[f'{warrior.name}_plus'] = self.game.display.blit(
                    IMAGES['button_plus'], (478 + offset, 438 + next_row - next_row * 0.061))
                self.army_shop_buttons[f'{warrior.name}_info'] = self.game.display.blit(
                    IMAGES['warrior_info'], (482 + offset, 322 + next_row))
                self.game.display.blit(warrior.image_right, field)
            # BLIT AND UPDATE
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()

    def shop_warrior(self, button_clicked):
        """
        This method lets characters buy new warriors to army (if enough money).
        """
        positions = [(392, 310), (525, 310), (658, 310), (259, 474), (392, 474), (525, 474), (658, 474)]
        warrior_name, postfix = button_clicked.split('_')
        warrior_fraction, warrior_number = warrior_name.split('-')
        warrior = WARRIORS[warrior_fraction[0].upper() + warrior_fraction[1:]][int(warrior_number) - 1]
        warrior_cost = warrior.cost
        field = IMAGES['warrior_table'].get_rect()
        field.topleft = positions[int(warrior_number) - 1]
        xp, yp = (positions[int(warrior_number) - 1][0] + 34, positions[int(warrior_number) - 1][1] + 46)
        if postfix == 'plus' and self.money >= warrior_cost:
            self.army[warrior] += 1
            self.money -= warrior_cost
        elif postfix == 'minus' and self.army[warrior] > 0:
            self.army[warrior] -= 1
            self.money += warrior_cost
        elif postfix == 'info':
            self.open_info = True
            while self.open_info:
                self.game.check_events()
                # TABLE AND WARRIOR NICKNAME
                self.game.display.blit(IMAGES['warrior_table'], field)
                self.game.draw_text(f'{warrior.nickname}', 22, xp + 32, yp - 16, 'c')
                # WARRIOR HEALTH
                self.game.display.blit(IMAGES['warrior_health'], (xp, yp))
                self.game.draw_text(f'{warrior.health}', 24, xp + 36, yp, 'tl')
                # WARRIOR ATTACK
                self.game.display.blit(IMAGES['warrior_attack'], (xp, yp + 36))
                self.game.draw_text(f'{warrior.attack}', 24, xp + 36, yp + 36, 'tl')
                # WARRIOR DEFENCE
                self.game.display.blit(IMAGES['warrior_defence'], (xp, yp + 72))
                self.game.draw_text(f'{warrior.defence}', 24, xp + 36, yp + 72, 'tl')
                # BLIT AND UPDATE
                self.game.window.blit(self.game.display, (0, 0))
                pygame.display.update()


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

    @staticmethod
    def draw_warrior_to_attack(character):
        return choice(character.alive_in_army(character))

    def turn_reward(self):
        self.experience += 50
        self.money += 50
        for warrior, i in zip(self.army, range(1, 8)):
            if 0 < i < 4:
                self.army[warrior] += 4
            elif 3 < i < 7:
                self.army[warrior] += 2
            elif i == 7:
                self.army[warrior] += 1
