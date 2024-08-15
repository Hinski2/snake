import pygame 
import random 
from enum import Enum 
from collections import namedtuple
import numpy as np

BLOCK_SIZE = 20
SPEED = 60
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 2 * BLOCK_SIZE)

class Direction(Enum):
    RIGHT = 1 
    LEFT = 2 
    UP = 3 
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

class SnakeGameAi:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h 
        
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        
        # init game state
        self.reset()
        
    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
    
        self.score = 0
        self.food = None
        self.place_food()
        self.frameIteration = 0
    
    def move(self, action): #action: [strainght, right, left]
        
        clock_direction = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_direction.index(self.direction)
        
        if np.array_equal(action, [1, 0, 0]): new_dir = clock_direction[idx]
        elif np.array_equal(action, [0, 1, 0]): new_dir = clock_direction[(idx + 1) % 4]
        elif np.array_equal(action, [0, 0, 1]): new_dir = clock_direction[(idx - 1) % 4]
        self.direction = new_dir 
         
        x, y = self.head.x, self.head.y 
        if self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT: x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN: y += BLOCK_SIZE
        elif self.direction == Direction.UP: y -= BLOCK_SIZE
        
        self.head = Point(x, y)
        
    def play_step(self, action):
        self.frameIteration += 1 
        
        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # move snake
        self.move(action)
        self.snake.insert(0, self.head)
        
        # check for game over
        reward = 0
        game_over = False
        if self.is_colision() or self.frameIteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        # place food
        if self.head == self.food:
            self.score += 1
            reward = 10 
            self.place_food()
        else: 
            self.snake.pop()
        
        # update clock
        self.update_ui()
        self.clock.tick(SPEED)
        
        #return
        return reward, game_over, self.score
    
    def is_colision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False
    
    def update_ui(self):
        self.display.fill((26, 255, 163))
        
        for pt in self.snake:
            pygame.draw.rect(self.display, (255, 255, 77), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.draw.rect(self.display, (204, 0, 102), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    
    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        
        # check if food spawned inside snake 
        if self.food in self.snake:
            self.place_food()

if __name__ == '__main__':
    game = SnakeGameAi()
    
    #game loop
    game_over = False
    while not game_over:
        game_over, score = game.play_step()
        
        if game_over: 
            print(f"final score = {score} GG")
        
        
    pygame.quit()
    