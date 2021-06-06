from menu import *
from character import *
from battle import Battle
from world import World
from structures.dijkstra import Dijkstra
from random import choice, randint
import pygame

FRACTIONS = {0: 'Demon', 1: 'Elf', 2: 'Human', 3: 'Undead'}

IMAGES = {'window_prompt': pygame.image.load('graphics/prompt_window.png'),
          'char_button': pygame.image.load('graphics/btn/char_button.png'),
          'army_button': pygame.image.load('graphics/btn/army_button.png'),
          'info_button': pygame.image.load('graphics/btn/info_button.png'),
          'settings_button': pygame.image.load('graphics/btn/settings_button.png'),
          'turn_button': pygame.image.load('graphics/btn/turn_button.png'),
          'yes_button': pygame.image.load('graphics/btn/yes_button.png'),
          'no_button': pygame.image.load('graphics/btn/no_button.png'),
          'interface': pygame.image.load('graphics/interface.png'),
          'map': pygame.image.load('graphics/map.png')}


class Game:
    """
    This class handle the game, display screen and make game loop.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The PyHero")
        pygame.mixer.music.load("music/song.ogg")
        pygame.mixer.music.play(-1)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1048, 792
        self.POSITIONS = [[[76 + 64 * j if i % 2 == 0 else 108 + 64 * j, 174 + 55 * i] for j in range(15)]
                          for i in range(13)]
        self.world = World(self)
        self.dij = Dijkstra(self.world.G)
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = 'graphics/FrederickaTheGreat.ttf'
        # Menu initialization
        self.MENUS = {'main_menu': MainMenu(self), 'game_menu': GameMenu(self), 'creator_menu': CreatorMenu(self),
                      'options_menu': OptionsMenu(self), 'credits_menu': CreditsMenu(self)}
        self.curr_menu = self.MENUS['main_menu']
        self.player, self.enemy = self.make_characters()
        self.turn, self.new_turn = 0, False
        self.battle_number, self.battle = 0, False
        self.prompt, self.prompt_answer = False, False
        self.answer = ''
        self.mx, self.my = 0, 0     # mouse position (mx, my)
        self.move = False
        self.map = None
        self.buttons = dict()

    def game_loop(self):
        """
        Method to start the game and handle all operations in game.
        """
        self.turn = 1
        self.player.flag = pygame.image.load(f"graphics/flags/{self.MENUS['creator_menu'].flag_number}_small.png")
        self.player.name = self.MENUS['creator_menu'].input_name
        self.player.fraction = self.MENUS['creator_menu'].fractions[self.MENUS['creator_menu'].fraction_number]
        while self.playing:
            self.draw_interface()
            self.check_events()
            if self.move:
                road = self.player.move((self.mx, self.my))
                if self.answer == 'yes' and not self.new_turn:
                    for r in road:
                        self.player.position = self.POSITIONS[r[0]][r[1]]
                        self.draw_interface()
                        self.window.blit(self.display, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(500)
            while self.player.position == self.enemy.position:
                self.battle = True
                self.battle_number += 1
                self.display.blit(IMAGES['map'], (12, 126))
                self.start_battle()
            while self.prompt:
                additional_text = ''
                if self.player.moves > 0:
                    additional_text = f'You still have {self.player.moves} moves!'
                self.open_prompt('Are you sure?', additional_text)
                if self.prompt_answer:
                    if self.answer == 'yes':
                        self.new_turn = True
                        self.prompt = False
                    else:
                        self.prompt = False
            if self.new_turn:
                road = self.enemy.make_move()
                for r in road:
                    self.enemy.position = self.POSITIONS[r[0]][r[1]]
                    self.draw_interface()
                    self.window.blit(self.display, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(500)
                self.turn += 1
                self.player.moves += self.add_moves()
                self.enemy.moves += self.add_moves()
                self.new_turn = False
            if self.ESCAPE_KEY:
                self.playing = False
                self.curr_menu = self.MENUS['creator_menu']
                self.curr_menu.run_display = True
                pygame.mouse.set_visible(False)
                self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
                self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True
                elif event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                """
                1 - left click
                2 - middle click
                3 - right click
                4 - scroll up
                5 - scroll down
                """
                self.mx, self.my = pygame.mouse.get_pos()
                if event.button == 1:
                    if self.map.collidepoint(self.mx, self.my) and not self.prompt:
                        self.move = True
                    elif self.buttons['char'].collidepoint(self.mx, self.my):
                        self.prompt = True
                    elif self.buttons['army'].collidepoint(self.mx, self.my):
                        self.prompt = True
                    elif self.buttons['info'].collidepoint(self.mx, self.my):
                        self.prompt = True
                    elif self.buttons['settings'].collidepoint(self.mx, self.my):
                        self.prompt = True
                    elif self.buttons['turn'].collidepoint(self.mx, self.my):
                        self.prompt = True
                    elif self.buttons['yes'].collidepoint(self.mx, self.my):
                        self.answer = 'yes'
                        self.prompt_answer = True
                        self.prompt = False
                    elif self.buttons['no'].collidepoint(self.mx, self.my):
                        self.answer = 'no'
                        self.prompt_answer = True
                        self.prompt = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.move = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def draw_interface(self):
        self.map = self.display.blit(IMAGES['map'], (12, 126))
        self.display.blit(IMAGES['interface'], (0, 0))
        self.draw_text(f'{self.player.name}', 40, 26, 14, text_format='tl')
        self.draw_text(f'| level: {self.player.level} ({self.player.experience}/100) |'
                       f' money: {self.player.money} |', 26, 28, 64, text_format='tl')
        self.draw_text(f'Turn: {self.turn}', 36, 768, 16, text_format='tl')
        self.draw_text(f'Moves: {self.player.moves}', 36, 768, 54, text_format='tl')
        self.buttons['char'] = self.display.blit(IMAGES['char_button'], (394, 20))
        self.buttons['army'] = self.display.blit(IMAGES['army_button'], (484, 20))
        self.buttons['info'] = self.display.blit(IMAGES['info_button'], (574, 20))
        self.buttons['settings'] = self.display.blit(IMAGES['settings_button'], (664, 20))
        self.buttons['turn'] = self.display.blit(IMAGES['turn_button'], (942, 20))
        self.display_flag(self.player.flag, self.player.position)
        self.display_flag(self.enemy.flag, self.enemy.position)

    def make_characters(self):
        player = Player(self, 'Name', 0, 'Demon', choice(self.POSITIONS[12]))
        flags_left = [i for i in range(8)]
        flags_left.remove(self.MENUS['creator_menu'].flag_number)
        fractions_left = ['Demon', 'Elf', 'Human', 'Undead']
        fractions_left.remove(self.MENUS['creator_menu'].fractions[self.MENUS['creator_menu'].fraction_number])
        enemy = Enemy(self, 'Enemy', choice(flags_left), choice(fractions_left), choice(self.POSITIONS[0]))
        return player, enemy

    def draw_text(self, text, size, x, y, text_format=None):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        if text_format == 'center' or text_format == 'c':
            text_rect.center = (x, y)
        elif text_format == 'top-left' or text_format == 'tl':
            text_rect.topleft = (x, y)
        self.display.blit(text_surface, text_rect)

    def open_prompt(self, text, additional_text=''):
        while self.prompt:
            self.check_events()
            if self.ESCAPE_KEY:
                self.prompt = False
                self.prompt_answer = False
            elif self.START_KEY:
                self.prompt = False
                self.prompt_answer = True
            self.draw_interface()
            self.display.blit(IMAGES['window_prompt'], (204, 256))
            self.buttons['yes'] = self.display.blit(IMAGES['yes_button'], (616, 350))
            self.buttons['no'] = self.display.blit(IMAGES['no_button'], (358, 350))
            self.draw_text(text, 32, 524, 278, text_format='c')
            if len(additional_text) > 0:
                self.draw_text(additional_text, 32, 524, 314, text_format='c')
            self.window.blit(self.display, (0, 0))
            pygame.display.update()

    def display_flag(self, flag, position):
        """
        Method to draw a flag with given color (number) on world map.
        Given position (tuple: x and y) is for bottom left corner of flag image.
        """
        flag_rect = flag.get_rect()
        flag_rect.bottomleft = position
        self.display.blit(flag, flag_rect)

    def add_moves(self):
        result = 0
        for _ in range(4):
            result += self.dice_roll()
        return int(result / 4)

    @staticmethod
    def dice_roll():
        return randint(1, 6)

    def start_battle(self):
        """
        This method is used to start a battle when player and enemy are on the same tile.
        """
        Battle(self, self.battle_number, self.player, self.enemy)
