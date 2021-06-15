import pygame


class Menu:
    """
    This class handle the operations in menu and how it works.
    """
    def __init__(self, game):
        self.game = game
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load("music/menu_music.ogg")
        pygame.mixer.music.play(-1)
        self.mid_width, self.mid_height = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.bg = pygame.image.load('graphics/menu.png')
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -96

    def draw_cursor(self):
        self.game.draw_text('->', 68, self.cursor_rect.x, self.cursor_rect.y, text_format='c')

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
