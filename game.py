import pygame
import os


class Game:
    def __init__(self):
        self.size = self.width, self.height = 1024, 768
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemies = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("world_map.png"))
        self.clicks = []

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(pos)

            self.draw()
        print(self.clicks)
        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        flag = pygame.image.load("graphic_assets/fantasy-strategy-2d-game-assets/PNG/flags/2.png")

        for p in self.clicks:
            pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)
            self.win.blit(flag, (p[0] - 2, p[1] - 115))
        pygame.display.update()


if __name__ == "__main__":
    g = Game()
    g.run()
