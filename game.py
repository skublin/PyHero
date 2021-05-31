from menu import *
from character import *
from battle import *
from random import choice
import pygame


# available positions (201) on world map (Tuple with x and y)
# it's a kind a matrix with every tile's center point
MAP_POSITIONS = [[[76 + 64 * j if i % 2 == 0 else 44 + 64 * j, 174 + 55 * i] for j in range(15 if i % 2 == 0 else 16)]
                 for i in range(13)]

FRACTIONS = {0: 'Demon', 1: 'Elf', 2: 'Human', 3: 'Undead'}

IMAGES = {'window_prompt': pygame.image.load('graphics/prompt_window.png'),
          'turn_button': pygame.image.load('graphics/turn_button.png'),
          'yes_button': pygame.image.load('graphics/yes_button.png'),
          'no_button': pygame.image.load('graphics/no_button.png'),
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
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = 'graphics/FrederickaTheGreat.ttf'
        # Menu initialization
        self.main_menu = MainMenu(self)
        self.game_menu = GameMenu(self)
        self.creator_menu = CreatorMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.player, self.enemy = self.make_characters()
        self.turn = 0
        self.new_turn = False
        self.battle_number = 0
        self.prompt = False
        self.prompt_answer = False
        self.mx, self.my = 0, 0     # mouse position, start at (0, 0)
        self.clicking = False
        self.map = None
        self.button_turn = None
        self.button_yes = None
        self.button_no = None
        self.button_tile = None

    def game_loop(self):
        """
        Method to start the game and handle all operations in game.
        """
        self.turn = 1
        self.player.flag = pygame.image.load(f'graphics/flags/{self.creator_menu.flag_number}_small.png')
        self.player.name = self.creator_menu.input_name
        self.player.fraction = self.creator_menu.fraction_number
        while self.playing:
            self.draw_interface()
            self.check_events()
            if self.ESCAPE_KEY:
                self.prompt = True
                self.open_prompt('Are you sure?')
                if self.prompt_answer:
                    self.prompt_answer = False
                    self.playing = False
                    pygame.mouse.set_visible(False)
                    self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
                    self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
            if self.clicking:
                self.player.position = self.closest_position((self.mx, self.my))
            while self.player.position == self.enemy.position:
                self.battle_number += 1
                self.start_battle()
            while self.prompt:
                additional_text = ''
                if self.player.moves > 0:
                    additional_text = f'You still have {self.player.moves} moves!'
                self.open_prompt('Are you sure?', additional_text)
                if self.prompt_answer:
                    self.turn += 1
                    self.prompt_answer = False
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
                    # self.clicking = True
                    if self.map.collidepoint(self.mx, self.my):
                        self.clicking = True
                    elif self.button_turn.collidepoint(self.mx, self.my):
                        self.prompt = True
                    elif self.button_yes.collidepoint(self.mx, self.my):
                        self.prompt_answer = True
                        self.prompt = False
                    elif self.button_no.collidepoint(self.mx, self.my):
                        self.prompt_answer = False
                        self.prompt = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def draw_interface(self):
        self.map = self.display.blit(IMAGES['map'], (12, 126))
        self.display.blit(IMAGES['interface'], (0, 0))
        self.draw_text(f'{self.player.name} ({FRACTIONS[self.player.fraction]}) ', 40, 24, 16, text_format='tl')
        self.draw_text(f'| level: {self.player.level} | experience: {self.player.experience} |'
                       f' money: {self.player.money}', 24, 28, 62, text_format='tl')
        self.draw_text(f'Turn: {self.turn}', 36, 768, 16, text_format='tl')
        self.draw_text(f'Moves: {self.player.moves}', 36, 768, 54, text_format='tl')
        self.button_turn = self.display.blit(IMAGES['turn_button'], (942, 20))
        self.display_flag(self.player.flag, self.player.position)
        self.display_flag(self.enemy.flag, self.enemy.position)

    def make_characters(self):
        player = Player(self, 'Name', 0, 0, (960, 830))
        flags_left = [i for i in range(8)]
        flags_left.remove(self.creator_menu.flag_number)
        fractions_left = [i for i in range(4)]
        fractions_left.remove(self.creator_menu.fraction_number)
        enemy = Enemy(self, 'Enemy', choice(flags_left), choice(fractions_left), choice(MAP_POSITIONS[0]))
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
            self.draw_interface()
            self.display.blit(IMAGES['window_prompt'], (204, 256))
            self.button_yes = self.display.blit(IMAGES['yes_button'], (616, 350))
            self.button_no = self.display.blit(IMAGES['no_button'], (358, 350))
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

    # it needs to be done better in some way (right algorithm or section of positions)
    def closest_position(self, click_point):
        """
        Method to determine which point of possible positions is the nearest one to clicked point.
        In other words it finds the center of a tile for given click point.
        """
        x, y = click_point
        minimum = 40
        closest_center = (0, 0)
        for row in MAP_POSITIONS:
            for position in row:
                xp, yp = position
                distance = ((xp - x)**2 + (yp - y)**2)**(1/2)
                if distance < minimum:
                    minimum = distance
                    closest_center = (xp, yp)
        return closest_center

    def start_battle(self):
        """
        This method is used to start a battle when player and enemy are on the same tile.
        """
        Battle(self, self.battle_number, self.player, self.enemy)
