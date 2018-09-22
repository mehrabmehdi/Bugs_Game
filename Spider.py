import pygame
import random


class Spider(pygame.sprite.Sprite):
    # initialize the spider Sprite
    # load its image
    # randomly spawns left or right
    image = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if Spider.image is None:
            Spider.image = pygame.image.load('Images/spider.png')
        self.image = Spider.image
        self.y = 500
        self.time = 0
        d2 = random.randint(1, 2)
        if d2 == 1:
            self.left_right = 'left'
            self.x = 0
        else:
            self.left_right = 'right'
            self.x = 625
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.speed = 15
        self.direction = 0

    def move(self):

        if self.time == 0:
            self.time = random.randint(2, 4)
            self.direction = random.randint(1, 4)

        # diagonal down
        if self.direction == 1:
            if self.left_right == 'left':
                self.x = self.x + self.speed
            else:
                self.x = self.x-self.speed
            self.y = self.y + self.speed/2
        # diagonal up
        if self.direction == 2:
            if self.left_right == 'left':
                self.x = self.x + self.speed
            else:
                self.x = self.x - self.speed
            self.y = self.y - self.speed/2
        # up
        if self.direction == 3:
            self.y = self.y-self.speed
        # down
        if self.direction == 4:
            self.y = self.y+self.speed
        if self.y > 649:
            if self.direction == 1:
                self.direction = 2
            else:
                self.direction = 3
        if self.y < 501:
            if self.direction == 2:
                self.direction = 1
            else:
                self.direction = 4

        self.time -= 1
        self.rect.topleft = (self.x, self.y)

    # checks if its offscreen or not
    def offscreen(self):
        if self.x < 0:
            return True
        if self.x > 625:
            return True
        else:
            return False
