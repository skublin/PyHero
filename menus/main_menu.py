from menu import Menu


class MainMenu(Menu):
    """
    A subclass of Menu to operate in the Main Menu after start of the program.
    """
    def __init__(self, game):
        super().__init__(game)
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
