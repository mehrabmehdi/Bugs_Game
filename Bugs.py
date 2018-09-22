import pygame
import random
from Centipede_part import *
from Tick import *
from Highscore import *
from Spider import *
from Background import *

# Global Variables

# Initializers
game_map = []
pygame.mixer.pre_init(44100, -16, 1, 64)
pygame.mixer.init()
pygame.init()
pygame.key.set_repeat(20, 20)
pygame.display.set_caption('Bugs')
# Images and sounds
mushroom_image = pygame.image.load('Images/mushroom.gif')
mushroom_image2 = pygame.image.load('Images/mushroom2.gif')
mushroom_image3 = pygame.image.load('Images/mushroom3.gif')
mushroom_image4 = pygame.image.load('Images/mushroom4.gif')
bug_hit = pygame.mixer.Sound('Sounds/bug_hit.wav')
player_death = pygame.mixer.Sound('Sounds/player_death.wav')
attack = pygame.mixer.Sound('Sounds/attack.wav')
mushroom_hit = pygame.mixer.Sound('Sounds/mushroom_hit.wav')
player_image = pygame.image.load('Images/wizard.png')
BackGround = Background('Images/background(2).png', [0,0])
screen = pygame.display.set_mode([625,700])
screen.fill([255, 255, 255])
screen.blit(BackGround.image, BackGround.rect)
# Fonts
titlefont = pygame.font.SysFont("Baskerville", 100)
instructtitlefont = pygame.font.SysFont("lato", 70)
instructfont = pygame.font.SysFont("purisa,", 15)
textfont = pygame.font.SysFont("Arial", 20)
scorefont = pygame.font.SysFont("Arial", 35)
# Game variables
level = 0
mode = 'menu'
shoot_x = 0
shoot_y = 0
time = 0
score = 0
spawning_centipedes = 0
can_shoot = True
player_x = 312
player_y = 650
pygame.mouse.set_visible(False)
running = True
mushrooms = []
centipede_parts = []
tick = 0
spider = Spider()

# To create text that can use newlines and text wraping
# Taken from:
# https://stackoverflow.com/questions/42014195/rendering-text-with-
# multiple-lines-in-pygame?rq=1
def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def setup_game_map():
    # Initialize music
    pygame.mixer.music.load('Sounds/gameplay.mp3')
    pygame.mixer.music.play(-1)
    global game_map
    game_map = []
    for x in range(0, 28):
        arrayOfZeros = [0]*25
        game_map.append(arrayOfZeros)
        # Randomly spawn 30 mushrooms
    for x in range(0, 30):
        mushroomx = random.randint(0, 24)
        mushroomy = random.randint(0, 21)
        mushrooms.append("mushroom")
        game_map[mushroomy][mushroomx] = 1

# if the mushrom is hit, the mushroom changes its immage to the next mushroom
# making a mushroom destroying animation
# when it is hit the 4th time it is completely destroyed


def draw_game_map():
        for column in range(25):
            for row in range(28):
                spot = game_map[row][column]
                if spot == 1:
                    screen.blit(mushroom_image, [column*25, row*25])
                if spot == 2:
                    screen.blit(mushroom_image2, [column*25, row*25])
                if spot == 3:
                    screen.blit(mushroom_image3, [column*25, row*25])
                if spot == 4:
                    screen.blit(mushroom_image4, [column*25, row*25])


# Player movement
def move():
    # Global variables for player position and mouse position
    global player_x, player_y, shoot_x, shoot_y, can_shoot
    pos = pygame.mouse.get_pos()

    # Boundaries for Player
    if game_map[int(pos[1]/25)][int(pos[0]/25)] == 0:
        player_x = pos[0]-6
        player_y = pos[1]-15
        if player_x > 564:
            player_x = 565
        if player_y > 634:
            player_y = 635
        if player_y < 536:
            player_y = 535

    shoot_y -= 25
    if shoot_y < 1:
        can_shoot = True

# the shooting function
def shoot(x, y):
    global shoot_x, shoot_y, can_shoot
    attack.play(loops=0, maxtime=0, fade_ms=0)
    shoot_x = x + 35
    shoot_y = y + 15
    can_shoot = False

# after it is shot
def is_shot():
    global shoot_x, shoot_y, can_shoot, score, tick
    shot_tilex = shoot_x/25
    shot_tiley = shoot_y/25

    # Check if hit mushroom
    # if a mushroom is hit, change its image to the next one
    # change can_shoot to true
    if game_map[int(shot_tiley)][int(shot_tilex)] > 0:
        mushroom_hit.play(loops=0, maxtime=0, fade_ms=0)
        game_map[int(shot_tiley)][int(shot_tilex)] += 1
        if game_map[int(shot_tiley)][int(shot_tilex)] == 5:
            game_map[int(shot_tiley)][int(shot_tilex)] = 0
        can_shoot = True
        shoot_x = 1000
        shoot_y = 800
        score += 1

    # Check if shot hit centipede
    for cp in centipede_parts:
        # if hit, delete the part of the centipede and spawn a mushroom
        # at that position
        if int(shot_tilex) == int(cp.x) and int(shot_tiley) == int(cp.y):
            bug_hit.play(loops=0, maxtime=0, fade_ms=0)
            centipede_parts.remove(cp)
            score += 10
            game_map[int(shot_tiley)][int(shot_tilex)] = 1
            can_shoot = True
            shoot_x = 1000
            shoot_y = 800
    # check if shot hit the spider
    # if hit, tick is dead
    if int(shot_tilex) == int(tick.x) and int(shot_tiley) == int(tick.y):
            bug_hit.play(loops=0, maxtime=0, fade_ms=0)
            score += 50
            can_shoot = True
            shoot_x = 1000
            shoot_y = 800
            tick.dead()
    # check if shot hit the spider
    # if hit, spider is dead
    if spider.rect.collidepoint((shoot_x, shoot_y)):
            bug_hit.play(loops=0, maxtime=0, fade_ms=0)
            score += 20
            can_shoot = True
            shoot_x = 1000
            shoot_y = 800
            spider.x = 10000


# Collision with bug for Player
def is_dead():
    global running, mode, topthreescores
    # Initialization has a plus 42 because we are using a top-down view. This
    # allows for the centipede to only collide with the player's feet instead
    # of hitting the player's head which would be strange. The centipede
    # collides with where the player is standing.
    player_rect = pygame.Rect(player_x+6, player_y + 42, 35, 20)
    for cp in centipede_parts:
        if player_rect.colliderect(cp.rect):
            player_death.play()
            pygame.time.delay(1000)
            mode = 'over'
            Highscore.write_score(score)
            topthreescores = Highscore.get_top_scores(3)
    if player_rect.colliderect(tick.rect) or player_rect.colliderect(spider.rect):
            player_death.play()
            pygame.time.delay(1000)
            mode = 'over'
            Highscore.write_score(score)
            topthreescores = Highscore.get_top_scores(3)

# makes the centipede


def make_centipede():
    global spawning_centipedes
    spawning_centipedes = 12

# draws the background and then the bugs onto the screen


def draw_everything():
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    message = textfont.render(str(score), 1, pygame.color.THECOLORS['red'])
    screen.blit(message, (20, 675))
    draw_game_map()
    pygame.draw.circle(screen, pygame.color.THECOLORS['blue'], (shoot_x, shoot_y), 5, 4)
    screen.blit(tick.image, tick.rect)
    screen.blit(spider.image, spider.rect)
    for cp in centipede_parts:
            screen.blit(cp.image, cp.rect)
    screen.blit(player_image, (player_x, player_y))
    pygame.display.update()

# if the centipede is completely killed, spawn another at the top
# increase the level(hence the difficulty so that ticks and spiders spawn more often)


def all_dead():
    global level
    if centipede_parts == []:
        make_centipede()
        level += 1


tick = Tick()
tick.dead()
topthreescores = Highscore.get_top_scores(3)


# Main Game
while running:
    pygame.time.delay(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False

        # Shooting
        keys = pygame.key.get_pressed()
        pressed = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or pressed[0] == True) and can_shoot == True:
            shoot(player_x, player_y+1)

    # For main menu screen
    if mode == 'menu':
        # Stop music and make mouse visible
        pygame.mixer.music.stop()
        pygame.mouse.set_visible(True)
        spider.x = 10000
        level = 1

        # Draw main menu screen and all text
        pygame.draw.rect(screen, pygame.color.THECOLORS['black'], (0, 0, 750, 840))
        main_title = titlefont.render("BUGS", 1, pygame.color.THECOLORS['white'])
        screen.blit(main_title, (230, 100))

        pygame.draw.rect(screen, pygame.color.THECOLORS['red'], (208, 233, 243, 38))
        pygame.draw.rect(screen, pygame.color.THECOLORS['yellow'], (210, 235, 238, 32))
        start = textfont.render("Click to Start the Game", 1, pygame.color.THECOLORS['black'])
        b = screen.blit(start, (220, 240))

        pygame.draw.rect(screen, pygame.color.THECOLORS['red'], (208, 297, 243, 38))
        pygame.draw.rect(screen, pygame.color.THECOLORS['yellow'], (210, 298, 238, 32))
        instruct = textfont.render("Click to Read Instructions", 1, pygame.color.THECOLORS['black'])
        c = screen.blit(instruct, (220, 300))

        highscoreText = textfont.render("Highscores", 1, pygame.color.THECOLORS['white'])
        a = screen.blit(highscoreText, (270, 400))
        Highscore.show_high_scores(pygame, screen, topthreescores, 300, 415)

        reset = textfont.render("Click to Reset Highscores", 1, pygame.color.THECOLORS['white'])
        d = screen.blit(reset, (220, 510))

        # Click interactions
        # Get mouse position
        mpos = pygame.mouse.get_pos()
        # Check if mouse clicked on "Start Game" and initialize the game elements
        if b.collidepoint(mpos):
            if event.type == pygame.MOUSEBUTTONUP:
                mode = 'play'
                time = 0
                centipede_parts = []
                score = 0
                tick.dead()
                setup_game_map()
        # Check if mouse clicked on Instructions
        if c.collidepoint(mpos):
            if event.type == pygame.MOUSEBUTTONUP:
                mode = 'instruct'
        # Check if mouse clicked on "Reset highscores" and remove everything
        # from highscore.txt
        if d.collidepoint(mpos):
            if event.type == pygame.MOUSEBUTTONUP:
                open('highscore.txt', 'w').close()

        # Update the display
        pygame.display.update()

    # If player clicked "Instructions"
    if mode == 'instruct':
        # Redraw black background and display the text using the blit_text
        # function found from stackoverflow
        pygame.draw.rect(screen, pygame.color.THECOLORS['black'], (0, 0, 750, 840))

        instruct_title = instructtitlefont.render("INSTRUCTIONS", 1, pygame.color.THECOLORS['white'])
        screen.blit(instruct_title, (70, 100))

        instructions_text = "You're a wizard Harry! Go do wizardly things " \
            "like keeping those damn bugs off your lawn.\nMove your wizardly" \
            " character by using the mouse. However, you can only move so " \
            "far up because your wizard powers only work when you are " \
            "near the magical snail, Karl.\nClick the left mouse button or"\
            " the space bar to shoot bolts of magic. Kill that damn " \
            "centipede that's been running around for so long and any " \
            "other bugs that appear. Watch out for that centipede though, " \
            "because it will split in two whenever you shoot it in the middle!"\
            " Spiders show up from the sides and some " \
            "ticks comes at you from the top too. "
        blit_text(screen, instructions_text, (30, 200), instructfont)

        back = textfont.render("Click to Return", 1, pygame.color.THECOLORS['white'])
        c = screen.blit(back, (220, 600))

        # If mouse clicks on "Return", go back to main menu
        mpos = pygame.mouse.get_pos()
        if c.collidepoint(mpos):
            if event.type == pygame.MOUSEBUTTONUP:
                mode = 'menu'
        pygame.display.update()

    # If player collides with any enemies, show this gameover screen
    if mode == 'over':
        # Set make cursor visible
        pygame.mouse.set_visible(True)

        # Draw everything that appears on screen including screen and
        # top five highscores
        pygame.draw.rect(screen, pygame.color.THECOLORS['black'], (0, 0, 750, 840))

        lost = titlefont.render("Game Over", 1, pygame.color.THECOLORS['white'])
        screen.blit(lost, (130, 100))

        final = textfont.render("Your score was:", 1, pygame.color.THECOLORS['white'])
        screen.blit(final, (250, 200))

        # Cast the score into a string because it requires a string instance
        scoretext = scorefont.render(str(score), 1, pygame.color.THECOLORS['white'])
        screen.blit(scoretext, (310, 230))

        highscores = textfont.render("Highscores", 1, pygame.color.THECOLORS['white'])
        screen.blit(highscores, (275, 280))
        topfivescores = Highscore.get_top_scores(5)
        Highscore.show_high_scores(pygame, screen, topfivescores, 300, 300)

        backOver = textfont.render("Click to Return to Menu", 1, pygame.color.THECOLORS['white'])
        overReturnButton = screen.blit(backOver, (220, 600))

        # If mouse clicks on "Return", go back to main menu
        mpos = pygame.mouse.get_pos()
        if overReturnButton.collidepoint(mpos):
            if event.type == pygame.MOUSEBUTTONUP:
                mode = 'menu'
        pygame.display.update()

    # If mouse clicked onto "Start Game"
    if mode == 'play':
        # Initialize player movement and collision
        move()
        is_dead()

        # Makes mouse invisible
        pygame.mouse.set_visible(False)
        # if random int in given range is zero
        # spawn the tick or spiders
        # as level increases, the range decrease, hence they spawn more often
        # therefore increasing the difficuly
        if random.randint(0, int(2000/level)) == 0:
            if tick.offscreen() is True:
                tick = Tick()
        if random.randint(0, int(1000/level)) == 0:
            if spider.offscreen() is True:
                spider = Spider()
        # checks if all dead every 3 itterations
        # done to decrease O runtime
        if time % 3 == 0:
            all_dead()
            # if all are dead, and centipede greater than 0
            # decrease it by 1 and spawn again
            if spawning_centipedes > 0:
                spawning_centipedes -= 1
                centipede_part = Centipede_part(12, 0)
                centipede_parts.append(centipede_part)
            # the movement of the bugs is called
            for cp in centipede_parts:
                cp.move(game_map)
            tick.move(game_map)
            spider.move()
        # if can_shoot is false, checks if it hit a mushroom
        # so that you can shoot again
        if can_shoot is False:
            is_shot()
        # increase the itteration
        time += 1
        # draw everything
        draw_everything()


pygame.quit()
