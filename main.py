import pygame
import time
#used to put the apple at the random position
import random
#for event looping
from pygame.locals import *

#size of the block and apple pictures, will be used later
size = 40
background_color = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        # it should be in multiple
        self.x = size*3
        self.y = size*3

    def draw(self):
        #fill method, we will apply in snake draw function
        # putting something on the surface- blit method
        self.parent_screen.blit(self.image, (self.x, self.y))
        # updating the code
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24)*size
        self.y = random.randint(0, 19)*size


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
    # loading image
        self.block = pygame.image.load("resources/block.jpg").convert()
    #placement of the block
        self.x = [40]*length
        self.y = [40]*length
    #used in walk def
        self.direction = 'down'

    def increase_length(self):
        #cause the last block will be the part of the walk() function
        self.length += 1
        #append some random value cause walk()function will take care of this
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        # putting something on the surface- blit method
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        # updating the code
        pygame.display.flip()

    def walk(self):
        #this for loop will not come after all the if statements because first two
        #blocks will have same place all the time so they will overlap
        #update body
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        #update head
        if self.direction == 'left':
            self.x[0] -= size
            if self.x[0] < 0:
                raise ValueError("GAME OVER")
        if self.direction == 'right':
            self.x[0] += size
            if self.x[0] >= 1000:
                raise ValueError("GAME OVER")
        if self.direction == 'up':
            self.y[0] -= size
            if self.y[0] < 0:
                raise ValueError("GAME OVER")
        if self.direction == 'down':
            self.y[0] += size
            if self.y[0] >= 800:
                raise ValueError("GAME OVER")

        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
    # setting the window size.......surface is the background
    # also used to clear the window screen back to just a background
        pygame.display.set_caption("SNAKE GAME")
        self.surface = pygame.display.set_mode((1000, 800))
    # window color
        self.play_background_music()
        self.surface.fill(background_color)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, x2, y1, y2):
        # the condition after 'and' will not be <= cause if snake passed by adjacent
        # to apple, then also it consider it as collision
        if (x1 >= x2) and (x1 < x2 + size):
            if (y1 >= y2) and (y1 < y2 + size):
                return True
        return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg music.mp3")
        pygame.mixer.music.play(-1)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (-300, -200))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.apple.x, self.snake.y[0], self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        #snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.x[i], self.snake.y[0], self.snake.y[i]):
                self.play_sound("crash")
                #raising an exception
                raise ValueError("GAME OVER")

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('ariel', 50)
        line1 = font.render(f"GAME OVER!! Your Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"Hit Enter To Play Again", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        line3 = font.render(f"Hit Escape To Quit", True, (255, 255, 255))
        self.surface.blit(line3, (200, 400))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def display_score(self):
        #choosing the font type for printing the score
        font = pygame.font.SysFont('ariel', 30,)
        #printing the score
        score = font.render(f"SCORE: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (890, 10))

    def run(self):
        #apply event loop
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except ValueError:
                self.game_over()
                pause = True
                self.reset()
            #without time sleep...block will disappear in lightning speed
            #so, to freeze the block for sometime, we use this
            time.sleep(0.15)


if __name__ == "__main__":

    #in this block we just want 2 or 3 lines or code
    #thatswhy we use oop system for this

    game = Game()
    game.run()
