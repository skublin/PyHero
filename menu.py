import pygame


class Menu:
    """
    This class handle the operations in menu and how it works.
    """
    def __init__(self, game):
        self.game = game
        self.mid_width, self.mid_height = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.bg = pygame.image.load('graphics/menu_bg.png')
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -130

    def draw_cursor(self):
        self.game.draw_text('->', 68, self.cursor_rect.x, self.cursor_rect.y)

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
        self.start_x, self.start_y = self.mid_width + 40, self.mid_height + 64
        self.options_x, self.options_y = self.mid_width + 1, self.mid_height + 110
        self.credits_x, self.credits_y = self.mid_width - 4, self.mid_height + 160
        self.quit_x, self.quit_y = self.mid_width + 33, self.mid_height + 206
        self.cursor_rect.midtop = (self.mid_width + self.offset, self.start_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 38)
            self.game.draw_text("Start Game", 44, self.start_x, self.start_y)
            self.game.draw_text("Options", 44, self.options_x, self.options_y)
            self.game.draw_text("Credits", 44, self.credits_x, self.credits_y)
            self.game.draw_text("Quit Game", 44, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.quit_y)
                self.state = "Quit Game"
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.start_y)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.quit_y)
                self.state = "Quit Game"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.start_y)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.mid_width + self.offset, self.credits_y)
                self.state = "Credits"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit Game':
                self.game.running = False
            self.run_display = False


class OptionsMenu(Menu):
    """
    A subclass of Menu to show Options for player.
    """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.vol_x, self.vol_y = self.mid_width + 40, self.mid_height + 64
        self.controls_x, self.controls_y = self.mid_width + 40, self.mid_height + 110
        self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 38)
            self.game.draw_text("Volume", 44, self.vol_x, self.vol_y)
            self.game.draw_text("Controls", 44, self.controls_x, self.controls_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controls_x + self.offset, self.controls_y)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)
        elif self.game.START_KEY:
            # GO TO SPECIFIC MENU
            pass


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
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 38)
            self.game.draw_text('Made by Szymon Kublin', 44, self.mid_width, self.mid_height + 80)
            self.blit_screen()
