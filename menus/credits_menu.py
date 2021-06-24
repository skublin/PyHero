from menu import Menu


class CreditsMenu(Menu):
    """
    A subclass of Menu just to show some credits.
    """
    def __init__(self, game):
        super().__init__(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            # BACK_KEY may be removed
            if self.game.START_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.MENUS['main_menu']
                self.run_display = False
            self.game.display.blit(self.bg, (0, 0))
            self.game.draw_text("The PyHero", 66, self.mid_width, self.mid_height - 36, text_format='c')
            self.game.draw_text('Author:', 44, self.mid_width, self.mid_height + 64, text_format='c')
            self.game.draw_text('Szymon Kublin', 44, self.mid_width, self.mid_height + 112, text_format='c')
            self.game.draw_text('Music:', 44, self.mid_width, self.mid_height + 170, text_format='c')
            self.game.draw_text('Free Music Archive', 44,
                                self.mid_width, self.mid_height + 218, text_format='c')
            self.game.draw_text('Graphic:', 44, self.mid_width, self.mid_height + 276, text_format='c')
            self.game.draw_text('CraftPix Assets', 44, self.mid_width, self.mid_height + 324, text_format='c')
            self.blit_screen()
