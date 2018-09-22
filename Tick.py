import pygame
import random


# Class of the Tick Sprite
class Tick(pygame.sprite.Sprite):

    image = None

    # initialize the Tick
    # load the image of the Tick
    # make it spawn randomly from anywhere at the top of the screen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if Tick.image is None:
            Tick.image = pygame.image.load("Images/tick.png")
        self.image = Tick.image
        self.x = random.randint(0, 24)
        self.y = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x*25, self.y*25)

    # defines its movement
    # if the randmon in in the range(0,2) is 1,
    # spawn a mushroom at that position
    def move(self, game_map):

        r = random.randint(0, 2)
        self.y += 1
        self.rect.topleft = (self.x*25, self.y*25)

        if self.y == 27:
            return
        if r == 1 and self.y < 26:
            game_map[self.y][self.x] = 1

    # if tick is deac, moves it off screen
    def dead(self):

        self.y = 100
        self.rect.topleft = (self.x*25, self.y*25)

    # checks if tick is offscreen
    def offscreen(self):
        if self.y > 28:
            return True
        else:
            return False
