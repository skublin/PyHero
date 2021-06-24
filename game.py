from menus.main_menu import MainMenu
from menus.game_menu import GameMenu
from menus.creator_menu import CreatorMenu
from menus.options_menu import OptionsMenu
from menus.credits_menu import CreditsMenu
from character import *
from battle import Battle
from world import World
from structures.dijkstra import Dijkstra
from random import choice, randint
import pygame

FRACTIONS = {0: 'Demon', 1: 'Elf', 2: 'Human', 3: 'Undead'}

IMAGES = {'window_prompt': pygame.image.load('graphics/prompt_window.png'),
          'character_prompt': pygame.image.load('graphics/character_prompt.png'),
          'army_prompt': pygame.image.load('graphics/army_prompt.png'),
          'faq_prompt': pygame.image.load('graphics/faq_prompt.png'),
          'char_button': pygame.image.load('graphics/btn/char_button.png'),
          'army_button': pygame.image.load('graphics/btn/army_button.png'),
          'info_button': pygame.image.load('graphics/btn/info_button.png'),
          'settings_button': pygame.image.load('graphics/btn/settings_button.png'),
          'turn_button': pygame.image.load('graphics/btn/turn_button.png'),
          'yes_button': pygame.image.load('graphics/btn/yes_button.png'),
          'no_button': pygame.image.load('graphics/btn/no_button.png'),
          'interface': pygame.image.load('graphics/interface.png'),
          'map': pygame.image.load('graphics/map.png'),
          'battleground': pygame.image.load('graphics/battleground_map.png'),
          'battle_sign': pygame.image.load('graphics/battle_sign.png'),
          'coin': pygame.image.load('graphics/coin.png'),
          'stars': pygame.image.load('graphics/stars.png')}


class Game:
    """
    This class handle the game, display screen and make game loop.
    """
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("The PyHero")
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
        self.player = Player(self, 'Name', 0, 'Human', choice(self.POSITIONS[12]))
        self.enemy = Enemy(self, 'Enemy', 1, 'Undead', choice(self.POSITIONS[0]))
        self.turn, self.new_turn = 0, False
        self.battle, self.battle_number, self.battle_mode = None, 0, False
        self.prompt, self.prompt_answer = False, False
        self.character_prompt, self.army_prompt, self.faq_prompt, self.settings_prompt = False, False, False, False
        self.answer = ''
        self.mx, self.my = 0, 0     # mouse position (mx, my)
        self.move = False
        self.map, self.battle_map = None, None
        self.buttons = dict()

    def game_loop(self):
        """
        Method to start the game and handle all operations in game.
        """
        self.turn = 1
        self.make_characters()
        while self.playing:
            # PREPARATION
            self.draw_interface()
            self.check_events()
            # CHECK IF LEVEL UP
            self.player.check_level_up()
            # CHECK MAP EVENTS BEFORE MOVE
            self.world.events_on_map()
            # PLAYER MOVE
            if self.move:
                road = self.player.move((self.mx, self.my))
                if self.answer == 'yes' and not self.new_turn:
                    self.show_moves(road, True, False)
            # CHECK MAP EVENTS AFTER MOVE
            self.world.events_on_map()
            # BATTLE
            if self.player.position == self.enemy.position:
                self.show_battle_sign()
                self.battle_mode = True
                self.battle_number += 1
                self.start_battle()
            # PROMPT WINDOW
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
            # PLAYER CARD PROMPT
            while self.character_prompt:
                self.player.character_info(IMAGES['character_prompt'])
                if self.ESCAPE_KEY:
                    self.ESCAPE_KEY = False
                    self.character_prompt = False
            # ARMY CARD PROMPT
            while self.army_prompt:
                self.player.army_info(IMAGES['army_prompt'])
                if self.ESCAPE_KEY:
                    self.ESCAPE_KEY = False
                    self.army_prompt = False
            # FAQ PROMPT
            while self.faq_prompt:
                self.show_faq()
            # SETTINGS PROMPT
            while self.settings_prompt:
                self.world.show_settings()
            # NEXT TURN (ALSO ENEMY MOVE)
            if self.new_turn:
                road = self.enemy.make_move()
                self.show_moves(road, False, True)
                self.turn += 1
                self.player.moves += self.add_moves()
                self.enemy.moves += self.add_moves()
                self.enemy.turn_reward()
                self.new_turn = False
            # QUIT GAME
            if self.ESCAPE_KEY:
                self.prompt = True
                self.ESCAPE_KEY = False
                self.open_prompt('Are you sure?', "It'll close the game!")
                if self.prompt_answer:
                    if self.answer == 'yes':
                        self.playing = False
                        self.prompt = False
                        self.curr_menu = self.MENUS['creator_menu']
                        self.curr_menu.run_display = True
                        pygame.mouse.set_visible(False)
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load("music/menu_music.ogg")
                        pygame.mixer.music.play(-1)
                        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
                        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
                    if self.answer == 'no':
                        self.prompt = False
            # GAMEPLAY UPDATE
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
                        self.character_prompt = True
                    elif self.buttons['army'].collidepoint(self.mx, self.my):
                        self.army_prompt = True
                    elif self.buttons['info'].collidepoint(self.mx, self.my):
                        self.faq_prompt = True
                    elif self.buttons['settings'].collidepoint(self.mx, self.my):
                        self.settings_prompt = True
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
                    # if statement to change player's character skills
                    if self.character_prompt:
                        for button in self.player.skill_buttons:
                            if self.player.skill_buttons[button].collidepoint(self.mx, self.my):
                                self.player.skill_change(button)
                    # implementation of add/remove player's warriors (just buttons as above in character info)
                    if self.army_prompt:
                        for button in self.player.army_shop_buttons:
                            if self.player.army_shop_buttons[button].collidepoint(self.mx, self.my):
                                self.player.shop_warrior(button)
                    if self.player.open_info:
                        self.player.open_info = False
                    if self.battle_mode:
                        # moving pointer
                        if self.battle.buttons['next_unit'].collidepoint(self.mx, self.my):
                            self.battle.next_unit_click()
                        # clicking on warriors - player's attack
                        for target, warrior in zip(self.battle.enemy_clickable_warriors, self.enemy.army):
                            if self.battle.enemy_clickable_warriors[target].collidepoint(self.mx, self.my):
                                self.battle.click_and_attack(warrior, (self.mx, self.my))
                    if self.settings_prompt:
                        for button in self.world.buttons:
                            if self.world.buttons[button].collidepoint(self.mx, self.my):
                                self.world.click_button(self.world.buttons[button])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.move = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def draw_interface(self):
        self.map = self.display.blit(IMAGES['map'], (12, 126))
        self.display.blit(IMAGES['interface'], (0, 0))
        self.draw_text(f'{self.player.name}', 40, 26, 14, text_format='tl')
        self.display.blit(IMAGES['stars'], (22, 70))
        self.display.blit(IMAGES['coin'], (222, 74))
        self.draw_text(f'{self.player.level} [{self.player.experience}/{self.player.to_level_up}]',
                       28, 78, 66, text_format='tl')
        self.draw_text(f'{self.player.money}', 28, 256, 66, text_format='tl')
        self.draw_text(f'Turn: {self.turn}', 36, 768, 16, text_format='tl')
        self.draw_text(f'Moves: {self.player.moves}', 36, 768, 54, text_format='tl')
        self.buttons['char'] = self.display.blit(IMAGES['char_button'], (394, 20))
        self.buttons['army'] = self.display.blit(IMAGES['army_button'], (484, 20))
        self.buttons['info'] = self.display.blit(IMAGES['info_button'], (574, 20))
        self.buttons['settings'] = self.display.blit(IMAGES['settings_button'], (664, 20))
        self.buttons['turn'] = self.display.blit(IMAGES['turn_button'], (942, 20))
        self.display_flag(self.player.flag, self.player.position)
        self.display_flag(self.enemy.flag, self.enemy.position)

    def show_moves(self, road, player, enemy):
        for r in road:
            if player:
                self.player.position = self.POSITIONS[r[0]][r[1]]
            if enemy:
                self.enemy.position = self.POSITIONS[r[0]][r[1]]
            self.draw_interface()
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            if not r == road[-1]:
                pygame.time.delay(self.world.game_speed)

    def show_battle_sign(self):
        pygame.mixer.music.load("music/fanfare.wav")
        pygame.mixer.music.play(1)
        battle_sign_rect = IMAGES['battle_sign'].get_rect()
        battle_sign_rect.center = self.player.position[0] + 12, self.player.position[1]
        self.display.blit(IMAGES['battle_sign'], battle_sign_rect)
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        pygame.time.delay(self.world.game_speed * 2)

    def make_characters(self, kind='both'):
        if kind == 'both' or 'player':
            self.player.flag = pygame.image.load(f"graphics/flags/{self.MENUS['creator_menu'].flag_number}_small.png")
            self.player.name = self.MENUS['creator_menu'].input_name
            self.player.fraction = self.MENUS['creator_menu'].fractions[self.MENUS['creator_menu'].fraction_number]
            self.player.make_army()
        if kind == 'both' or 'enemy':
            flags_left = [i for i in range(8)]
            flags_left.remove(self.MENUS['creator_menu'].flag_number)
            fractions_left = ['Demon', 'Elf', 'Human', 'Undead']
            fractions_left.remove(self.MENUS['creator_menu'].fractions[self.MENUS['creator_menu'].fraction_number])
            self.enemy.flag = pygame.image.load(f"graphics/flags/{choice(flags_left)}_small.png")
            self.enemy.fraction = choice(fractions_left)
            self.enemy.make_army()

    def draw_text(self, text, size, x, y, text_format=None, text_color='black'):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (0, 0, 0))
        if text_color == 'white':
            text_surface = font.render(text, True, (255, 255, 255))
        elif text_color == 'red':
            text_surface = font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        if text_format == 'center' or text_format == 'c':
            text_rect.center = (x, y)
        elif text_format == 'top-left' or text_format == 'tl':
            text_rect.topleft = (x, y)
        elif text_format == 'bottom-left' or text_format == 'bl':
            text_rect.bottomleft = (x, y)
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
        self.battle_map = IMAGES['battleground']
        self.battle = Battle(self, self.battle_map, IMAGES['interface'], self.battle_number, self.player, self.enemy)
        self.battle.battle_loop()

    def show_faq(self):
        self.check_events()
        if self.ESCAPE_KEY:
            self.ESCAPE_KEY = False
            self.faq_prompt = False
        self.draw_interface()
        self.display.blit(IMAGES['faq_prompt'], (204, 256))
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
