import random
import sys, time
import flappy_bird.flappy_graphics as fg


class flappy(object):
    """object to hold the state of the flappy game"""
    def __init__(self):
        super(flappy, self).__init__()
        self.fps = 30
        self.screen_width  = 288
        self.screen_height = 512

        self.graphics = fg.graphics(self)
        self.graphics.load_images()

        self.initialize_game()
        self.graphics.load_images()
        self.graphics.initialize_display()


    def initialize_game(self):        
        self.pipe_gap  = 100 # gap between upper and lower part of pipe
        self.ground_y  = self.screen_height * 0.79

        self.bird_height = self.graphics.images['player'][0].get_height()
        self.bird_width  = self.graphics.images['player'][0].get_width()
        self.pipe_width  = self.graphics.images['pipe'][0].get_width()
        self.pipe_height = self.graphics.images['pipe'][0].get_height()


        self.x_bird = int(self.screen_width * 0.2)
        self.y_bird = int((self.screen_height - self.bird_height) / 2)


        self.basex    = 10
        self.playerIndexGen = 0

        self.game_over = False

        self.score = self.playerIndex = self.loopIter = 0
        self.x_bird = int(self.screen_width * 0.2)

        self.baseShift = self.graphics.images['base'].get_width() - self.graphics.images['background'].get_width()

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        # list of upper pipes
        self.upperPipes = [
            {'x': self.screen_width + 200, 'y': newPipe1[0]['y']},
            {'x': self.screen_width + 200 + (self.screen_width / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lowerpipe
        self.lowerPipes = [
            {'x': self.screen_width + 200, 'y': newPipe1[1]['y']},
            {'x': self.screen_width + 200 + (self.screen_width / 2), 'y': newPipe2[1]['y']},
        ]

        self.pipeVelX = -4

        # player velocity, max velocity, downward accleration, accleration on flap
        self.playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY =  10   # max vel along Y, max descend speed
        self.playerMinVelY =  -8   # min vel along Y, max ascend speed
        self.playerAccY    =   1   # players downward accleration
        self.playerFlapAcc =  -9   # players speed on flapping
        self.playerFlapped = False # True  when player flaps


    def flap(self):
        self.playerFlapped = True
            
    def check_crash(self):
        """returns score and ends game if player collides with base or pipes."""
        if (self.y_bird + self.bird_height >= self.ground_y) or self.y_bird <= 0:
            self.end_game()

        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            front_edge = self.x_bird + self.bird_width >= uPipe['x']
            back_edge  = self.x_bird <= uPipe['x'] + self.pipe_width
            if front_edge and back_edge:
                top_edge    =  self.y_bird <= uPipe['y'] + self.pipe_height # +y down!!
                bottom_edge =  self.y_bird + self.bird_height >= lPipe['y']
                if top_edge or bottom_edge:
                    print(top_edge, bottom_edge)
                    print(self.x_bird + self.bird_width, self.y_bird + self.bird_height, uPipe, lPipe)
                    self.end_game()


    def end_game(self):
        self.game_over = True
        self.graphics.show_score()
        self.graphics.update_display()


    def move_screen(self):
        # move bottom streak
        self.basex = -((-self.basex + 100) % self.baseShift)
        # player's movement
        if self.playerFlapped:
            self.playerVelY = self.playerFlapAcc
        elif self.playerVelY < self.playerMaxVelY:
            self.playerVelY += self.playerAccY
        self.y_bird += min(self.playerVelY, self.ground_y - self.y_bird - self.bird_height)
        self.playerFlapped = False

        # move pipes to left
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            uPipe['x'] += self.pipeVelX
            lPipe['x'] += self.pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upperPipes[0]['x'] < 5:
            newPipe = self.getRandomPipe()
            self.upperPipes.append(newPipe[0])
            self.lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if self.upperPipes[0]['x'] < -self.pipe_width:
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)

    def update_score(self):# check for score
        playerMidPos = self.x_bird + self.bird_width / 2
        for pipe in self.upperPipes:
            pipeMidPos = pipe['x'] + self.pipe_width / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                self.score += 1


    def getRandomPipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(self.ground_y * 0.6 - self.pipe_gap))
        gapY += int(self.ground_y * 0.2)
        pipeX = self.screen_width + 10

        return [
            {'x': pipeX, 'y': gapY - self.pipe_height},  # upper pipe
            {'x': pipeX, 'y': gapY + self.pipe_gap}, # lower pipe
        ]






    



