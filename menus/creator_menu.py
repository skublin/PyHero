from menu import Menu
from pygame_input import TextInput
import pygame


class CreatorMenu(Menu):
    """
    This is a class to make a new character, it's a subclass of Menu.
    It allows user to pick a name, flag color and fraction.
    """
    def __init__(self, game):
        super().__init__(game)
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
                pygame.mixer.music.unload()
                pygame.mixer.music.load("music/game_music.ogg")
                pygame.mixer.music.play(-1)
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
