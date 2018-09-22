class Highscore():
    # gets the highscores by reading the highscore.txt file
    # stores them on a list and sorts the in descending order
    # returns the top number of scores requested in an list
    @staticmethod
    def get_top_scores(number):
        everyscore = []
        with open('highscore.txt', 'r') as f:
            for line in f:
                everyscore.append(int(line.strip()))

        everyscore.sort()
        everyscore.reverse()
        topscores = everyscore[0:number]
        print(topscores)
        return topscores
    # writes the new score you got onto the highscore.txt file

    @staticmethod
    def write_score(score):
        with open('highscore.txt', 'a') as file_:
            file_.write(str(score)+'\n')
    # shows the list of highscore on the screen, in Ariel size 20,
    # displyas it at the given co-ordinates
    
    @staticmethod
    def show_high_scores(pygame, screen, list_of_scores, x, start_y):
        myfont = pygame.font.SysFont("Arial", 20)
        i = 1
        for top_score in list_of_scores:
            message = myfont.render(str(i) + '. '+str(top_score), 1, pygame.color.THECOLORS['white'])
            screen.blit(message, (x, start_y + 20*i))
            i += 1
