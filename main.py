import pygame 
import random 
from enum import Enum 
from collections import namedtuple

BLOCK_SIZE = 20
SPEED = 15
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 2 * BLOCK_SIZE)

class Direction(Enum):
    RIGHT = 1 
    LEFT = 2 
    UP = 3 
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

class SnakeGame():
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h 
        
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
    
        self.score = 0
        self.food = None
        self.place_food()
    
    def move(self, dir):
        x, y = self.head.x, self.head.y 
        if dir == Direction.RIGHT: x += BLOCK_SIZE
        elif dir == Direction.LEFT: x -= BLOCK_SIZE
        elif dir == Direction.DOWN: y += BLOCK_SIZE
        elif dir == Direction.UP: y -= BLOCK_SIZE
        
        self.head = Point(x, y)
        
    def play_step(self):
        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT: self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP: self.direction = Direction.UP 
                elif event.key == pygame.K_DOWN: self.direction = Direction.DOWN
                
        # move snake
        self.move(self.direction)
        self.snake.insert(0, self.head)
        
        # check for game over
        game_over = False
        if self.is_colision():
            game_over = True
            return game_over, score
        
        # place food
        if self.head == self.food:
            self.score += 1 
            self.place_food()
        else: 
            self.snake.pop()
        
        # update clock
        self.update_ui()
        self.clock.tick(SPEED)
        
        #return
        return False, self.score
    
    def is_colision(self):
        if self.head.x > self.w - BLOCK_SIZE: return True 
        if self.head.x < 0: return True 
        if self.head.y > self.h - BLOCK_SIZE: return True 
        if self.head.y < 0: return True
        
        if self.head in self.snake[1:]: return True
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
    game = SnakeGame()
    
    #game loop
    game_over = False
    while not game_over:
        game_over, score = game.play_step()
        
        if game_over: 
            print(f"final score = {score} GG")
        
        
    pygame.quit()
    