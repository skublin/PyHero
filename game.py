from menu import *
from character import *
from random import choice
import pygame


# available positions (201) on world map (Tuple with x and y)
MAP_POSITIONS = [[(76 + 64 * j if i % 2 == 0 else 44 + 64 * j, 174 + 55.5 * i) for j in range(15 if i % 2 == 0 else 16)]
                 for i in range(13)]


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
        self.world_map = pygame.image.load('graphics/world.png')
        self.font_name = 'graphics/FrederickaTheGreat.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.game_menu = GameMenu(self)
        self.creator_menu = CreatorMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.player, self.enemy = self.make_characters()

    def game_loop(self):
        """
        A basic function to start the game.
        """
        self.player.flag = pygame.image.load(f'graphics/flags/{self.creator_menu.flag_number}_small.png')
        self.player.name = self.creator_menu.input_name
        self.player.fraction = self.creator_menu.fraction_number
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
                self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
                self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
            self.display.blit(self.world_map, (0, 0))
            self.display_flag(self.player.flag, self.player.position)
            self.display_flag(self.enemy.flag, self.enemy.position)
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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def make_characters(self):
        player = Player(self, 'Name', 0, 0, choice(MAP_POSITIONS[12]))
        flags_left = [i for i in range(8)]
        flags_left.remove(self.creator_menu.flag_number)
        fractions_left = [i for i in range(4)]
        fractions_left.remove(self.creator_menu.fraction_number)
        enemy = Enemy(self, 'Enemy', choice(flags_left), choice(fractions_left), choice(MAP_POSITIONS[0]))
        return player, enemy

    def draw_text(self, text: str, size: int, x: int, y: int) -> None:
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        if text not in ['->', 'The PyHero'] and self.curr_menu != self.credits:
            text_rect.left = 460
        self.display.blit(text_surface, text_rect)

    def display_flag(self, flag, position):
        """
        Method to draw a flag with given color (number) on world map.
        Given position (tuple: x and y) is for bottom left corner of image.
        """
        flag_rect = flag.get_rect()
        flag_rect.bottomleft = position
        self.display.blit(flag, flag_rect)
