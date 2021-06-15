from menu import Menu


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
