import pygame


class Centipede_part(pygame.sprite.Sprite):

    image = None
    # initialize the centipede_part
    # load the image_file
    # declare initial directions

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        if Centipede_part.image is None:
            Centipede_part.image = pygame.image.load("Images/centipede.png")
        self.image = Centipede_part.image
        self.x = x
        self.y = y
        self.direction = 'right'
        self.heading = 'down'
        self.up_down_next_move = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x*25, self.y*25)

    def move(self, game_map):

        # moving right and not up or down
        if self.direction == 'right' and self.up_down_next_move == False:
            self.x += 1

            # hit mushroom
            if game_map[self.y][self.x] != 0:
                self.direction = 'left'

                if self.heading == 'down':
                    self.y += 1
                else:
                    self.y -= 1
                self.x -= 1
                if self.x == 0:
                    self.direction = 'right'

            # hit right wall
            if self.x == 24:
                self.direction = 'left'
                self.up_down_next_move = True
                # hit bottom
                if self.y == 27:
                    self.heading = 'up'
                # hit limit
            if self.y == 22:
                self.heading = 'down'

        # moving left not up or down
        elif self.direction == 'left' and self.up_down_next_move == False:
            self.x -= 1
            # hit mushroom
            if game_map[self.y][self.x] != 0:
                self.direction = 'right'

                if self.heading == 'down':
                    self.y += 1
                else:
                    self.y -= 1
                self.x += 1
                if self.x == 24:
                    self.direction = 'left'
            # hit left wall
            if self.x == 0:
                self.direction = 'right'
                self.up_down_next_move = True
                # hit bottom
                if self.y == 27:
                    self.heading = 'up'
                # hit limit
            if self.y == 22:
                self.heading = 'down'

        else:
            if self.heading == 'down':
                self.y += 1
            else:
                self.y -= 1
            self.up_down_next_move = False

        self.rect.topleft = (self.x*25, self.y*25)
