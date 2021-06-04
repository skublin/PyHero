import pygame
from pygame_input import TextInput


class Menu:
    """
    This class handle the operations in menu and how it works.
    """
    def __init__(self, game):
        self.game = game
        self.mid_width, self.mid_height = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.bg = pygame.image.load('graphics/menu.png')
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -96
        pygame.mouse.set_visible(False)

    def draw_cursor(self):
        self.game.draw_text('->', 68, self.cursor_rect.x, self.cursor_rect.y, text_format='c')

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    """
    A subclass of Menu to operate in the Main Menu after start of the program.
    """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 36, text_format='c')
            self.game.draw_text("Start Game", 44, self.mid_width - 48, self.mid_height + 38, text_format='tl')
            self.game.draw_text("Options", 44, self.mid_width - 48, self.mid_height + 86, text_format='tl')
            self.game.draw_text("Credits", 44, self.mid_width - 48, self.mid_height + 134, text_format='tl')
            self.game.draw_text("Quit Game", 44, self.mid_width - 48, self.mid_height + 182, text_format='tl')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 208)
                self.state = "Quit Game"
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 208)
                self.state = "Quit Game"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = "Options"
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = "Credits"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.MENUS['game_menu']
            elif self.state == 'Options':
                self.game.curr_menu = self.game.MENUS['options_menu']
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.MENUS['credits_menu']
            elif self.state == 'Quit Game':
                self.game.running = False
            self.run_display = False


class GameMenu(Menu):
    """
    A subclass of Menu to handle start of new game, load game and character creation.
    """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'New Game'
        self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 36, text_format='c')
            self.game.draw_text("New Game", 44, self.mid_width - 48, self.mid_height + 38, text_format='tl')
            self.game.draw_text("Load Game", 44, self.mid_width - 48, self.mid_height + 86, text_format='tl')
            self.game.draw_text("Back", 44, self.mid_width - 48, self.mid_height + 134, text_format='tl')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'New Game':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = 'Load Game'
            elif self.state == 'Load Game':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = 'Back'
            elif self.state == 'Back':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = 'New Game'
        elif self.game.UP_KEY:
            if self.state == "New Game":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = "Back"
            elif self.state == "Load Game":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = "New Game"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = "Load Game"

    def check_input(self):
        self.move_cursor()
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.MENUS['main_menu']
            self.run_display = False
            self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
        elif self.game.START_KEY:
            if self.state == 'New Game':
                self.game.curr_menu = self.game.MENUS['creator_menu']
            elif self.state == 'Load Game':
                # connection to database
                pass
            elif self.state == 'Back':
                self.game.curr_menu = self.game.MENUS['main_menu']
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
            self.run_display = False


class CreatorMenu(Menu):
    """
    This is a class to make a new character, it's a subclass of Menu.
    It allows user to pick a name, flag color and fraction.
    """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Name'
        self.input_name = ''
        self.flag_number = 0
        self.fraction_number = 0
        self.fractions = ['Demon', 'Elf', 'Human', 'Undead']
        self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 36, text_format='c')
            self.game.draw_text(self.input_name if self.input_name else "Pick Name",
                                44, self.mid_width - 48, self.mid_height + 38, text_format='tl')
            self.game.draw_text("Flag Color", 44, self.mid_width - 48, self.mid_height + 86, text_format='tl')
            self.game.draw_text("Fraction", 44, self.mid_width - 48, self.mid_height + 134, text_format='tl')
            self.game.draw_text("Let's go!", 44, self.mid_width - 48, self.mid_height + 182, text_format='tl')
            self.game.draw_text("Back", 44, self.mid_width - 48, self.mid_height + 230, text_format='tl')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Name':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = 'Color'
            elif self.state == 'Color':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = 'Fraction'
            elif self.state == 'Fraction':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 208)
                self.state = 'Go'
            elif self.state == 'Go':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 256)
                self.state = 'Back'
            elif self.state == 'Back':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = 'Name'
        elif self.game.UP_KEY:
            if self.state == "Name":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 256)
                self.state = "Back"
            elif self.state == "Color":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = "Name"
            elif self.state == "Fraction":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = "Color"
            elif self.state == "Go":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = "Fraction"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 208)
                self.state = "Go"

    def check_input(self):
        self.move_cursor()
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.MENUS['game_menu']
            self.run_display = False
            self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
        elif self.game.START_KEY:
            if self.state == 'Name':
                self.input_name = self.text_input()
                while len(self.input_name) > 12:
                    self.input_name = self.text_input()
            elif self.state == 'Color':
                self.flag_number = self.flag_picker()
            elif self.state == 'Fraction':
                self.fraction_number = self.fraction_picker()
            elif self.state == 'Go':
                while 1 > len(self.input_name) or len(self.input_name) > 12:
                    self.input_name = self.text_input()
                self.run_display = False
                self.game.playing = True
                pygame.mouse.set_visible(True)
                self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H + 114))
                self.game.window = pygame.display.set_mode((self.game.DISPLAY_W, self.game.DISPLAY_H + 114))
            elif self.state == 'Back':
                self.game.curr_menu = self.game.MENUS['game_menu']
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.reset_creator()
            self.run_display = False

    @staticmethod
    def text_input():
        """
        Method to enable player to type the name of character.
        It overrides first text in CreatorMenu ('Pick Name') with loaded character name.
        This method use TextInput class from pygame_input.py file.
        """
        text_input = TextInput()
        prompt_bg = pygame.image.load('graphics/name_prompt.png')
        screen = pygame.display.set_mode((512, 331))
        screen.blit(prompt_bg, (0, 0))
        pygame.display.update()
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((1024, 768))
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.display.set_mode((1024, 768))
                        return text_input.input_string
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((1024, 768))
                        return
            screen.blit(prompt_bg, (0, 0))
            text_input.update(events)
            screen.blit(text_input.get_surface(), (84, 184))
            pygame.display.update()
            clock.tick(30)

    def flag_picker(self):
        """
        Method to enable player to pick flag color. It shows a small window with possible flags.
        It loads flags from /graphics/flags/ and scales it to proper resolution.
        """
        flags = [pygame.image.load(f'graphics/flags/{i}.png') for i in range(8)]
        arrows = [pygame.transform.rotate(pygame.image.load('graphics/btn/arrow_button.png'), 90),
                  pygame.transform.rotate(pygame.image.load('graphics/btn/arrow_button.png'), -90)]
        prompt_bg = pygame.image.load('graphics/empty_prompt.png')
        screen = pygame.display.set_mode((512, 331))
        screen.blit(prompt_bg, (0, 0))
        pygame.display.update()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((1024, 768))
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.display.set_mode((1024, 768))
                        return self.flag_number
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((1024, 768))
                        return
                    elif event.key == pygame.K_RIGHT:
                        if self.flag_number == 7:
                            self.flag_number = 0
                        else:
                            self.flag_number += 1
                    elif event.key == pygame.K_LEFT:
                        if self.flag_number == 0:
                            self.flag_number = 7
                        else:
                            self.flag_number -= 1
            screen.blit(prompt_bg, (0, 0))
            screen.blit(flags[self.flag_number], (196, 104))
            screen.blit(arrows[0], (50, 124))
            screen.blit(arrows[1], (371, 124))
            pygame.display.update()

    def fraction_picker(self):
        """
        Method to enable player to choose the army fraction.
        It overrides third text in CreatorMenu ('Fraction') with chosen fraction name.
        """
        fraction_images = [pygame.image.load(f'graphics/fractions/{i}.png') for i in range(4)]
        arrows = [pygame.transform.rotate(pygame.image.load('graphics/btn/arrow_button.png'), 90),
                  pygame.transform.rotate(pygame.image.load('graphics/btn/arrow_button.png'), -90)]
        prompt_bg = pygame.image.load('graphics/empty_prompt.png')
        screen = pygame.display.set_mode((512, 331))
        screen.blit(prompt_bg, (0, 0))
        pygame.display.update()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((1024, 768))
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.display.set_mode((1024, 768))
                        return self.fraction_number
                    elif event.key == pygame.K_ESCAPE:
                        pygame.display.set_mode((1024, 768))
                        return
                    elif event.key == pygame.K_RIGHT:
                        if self.fraction_number == 3:
                            self.fraction_number = 0
                        else:
                            self.fraction_number += 1
                    elif event.key == pygame.K_LEFT:
                        if self.fraction_number == 0:
                            self.fraction_number = 3
                        else:
                            self.fraction_number -= 1
            screen.blit(prompt_bg, (0, 0))
            screen.blit(fraction_images[self.fraction_number], (200, 90))
            screen.blit(arrows[0], (50, 124))
            screen.blit(arrows[1], (371, 124))
            pygame.display.update()

    def reset_creator(self):
        self.input_name, self.flag_number, self.fraction_number = '', 0, 0


class OptionsMenu(Menu):
    """
    A subclass of Menu to show Options for player.
    """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 36, text_format='c')
            self.game.draw_text("Volume", 44, self.mid_width - 48, self.mid_height + 38, text_format='tl')
            self.game.draw_text("Controls", 44, self.mid_width - 48, self.mid_height + 86, text_format='tl')
            self.game.draw_text("Back", 44, self.mid_width - 48, self.mid_height + 134, text_format='tl')
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = 'Back'
            elif self.state == 'Back':
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = 'Volume'
        elif self.game.UP_KEY:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 160)
                self.state = "Back"
            elif self.state == "Controls":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
                self.state = "Volume"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 112)
                self.state = "Controls"
        elif self.game.START_KEY:
            if self.state == 'Volume':
                # sound settings
                pass
            elif self.state == 'Controls':
                # settings of controls
                pass

    def check_input(self):
        self.move_cursor()
        # BACK_KEY may be removed
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.MENUS['main_menu']
            self.cursor_rect.midtop = (self.mid_width + self.offset, self.mid_height + 64)
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Volume':
                # sound settings
                pass
            elif self.state == 'Controls':
                # settings of controls
                pass
            elif self.state == 'Back':
                self.game.curr_menu = self.game.MENUS['main_menu']
                self.run_display = False


class CreditsMenu(Menu):
    """
    A subclass of Menu just to show some credits.
    """
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            # BACK_KEY may be removed
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.MENUS['main_menu']
                self.run_display = False
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 36, text_format='c')
            self.game.draw_text('Author:', 44, self.mid_width, self.mid_height + 64, text_format='c')
            self.game.draw_text('Szymon Kublin', 44, self.mid_width, self.mid_height + 112, text_format='c')
            self.game.draw_text('Music:', 44, self.mid_width, self.mid_height + 170, text_format='c')
            self.game.draw_text('Pictures of the Floating World', 44,
                                self.mid_width, self.mid_height + 218, text_format='c')
            self.game.draw_text('Graphic:', 44, self.mid_width, self.mid_height + 276, text_format='c')
            self.game.draw_text('CraftPix Assets', 44, self.mid_width, self.mid_height + 324, text_format='c')
            self.blit_screen()
