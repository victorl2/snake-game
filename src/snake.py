import src.logger as logger
from typing import Final
import logging as log
import numpy as np
import pygame

# Colors
LIGHT_BLUE: Final = (56, 212, 218)
LIGHT_GREY: Final = (200, 200, 200)
BLACK: Final = (0, 0, 0)
WHITE: Final = (255, 255, 255)
DARK_GREEN: Final = (0, 100, 0)
RED: Final = (255, 0, 0)

# Game settings
FRUIT_TILE: Final = -1
EMPTY_TILE: Final = 0

class Game:


    def __init__(self, board_size = 32, headless=False):
        self.width = 800
        self.height = 800
        self.headless = headless
        self.running = False
        self.screen = None
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=np.int8)
        self.score = 0
        self.board[6, board_size // 2] = 1 # add snake on the board
        self._add_food() 
       

    def run(self):
        """ main game loop """
        self.__initialize()
        # Event handling
        while self.running:
            for event in pygame.event.get():
                self.__handle_event(event)
            self.__draw()
        pygame.quit()
    

    def __handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False

    def __draw(self):
        if self.headless:
            return
        
        self.screen.fill(WHITE) # Fill the background with white

        # draw a grid
        for x in range(0, self.width, self.width // self.board_size):
            pygame.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, self.height))
            for y in range(0, self.height, self.height // self.board_size):
                pygame.draw.line(self.screen, LIGHT_GREY, (0, y), (self.width, y))
        
        for x in range(self.board_size):
            for y in range(self.board_size):
                if x == 0 or y == 0 or x == self.board_size - 1 or y == self.board_size - 1:
                    pygame.draw.rect(self.screen, BLACK, (x * self.width // self.board_size, y * self.height // self.board_size, self.width // self.board_size, self.height // self.board_size))

        # draw the snake
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x, y] > 0:
                    pygame.draw.rect(self.screen, DARK_GREEN, (x * self.width // self.board_size, y * self.height // self.board_size, self.width // self.board_size, self.height // self.board_size))
                elif self.board[x, y] == FRUIT_TILE:
                    pygame.draw.rect(self.screen, RED, (x * self.width // self.board_size, y * self.height // self.board_size, self.width // self.board_size, self.height // self.board_size))
        
        # draw the score on the screen
        font = pygame.font.Font(None, 30)
        text = font.render("score: " + str(self.score), 1, LIGHT_BLUE)
        self.screen.blit(text, (10, 2))

        pygame.display.flip()
    

    def __initialize(self):
        """ basic initialization for the game window and pygame itself """
        logger.config_log()
        log.info("initializing snake game")
        pygame.init()

        if not self.headless:
            self.screen = pygame.display.set_mode([self.width, self.height])
            pygame.display.set_caption("Snake")
            log.info("screen dimensions set to %s", self.screen.get_size())
        else:
            log.info("headless mode enabled")
        
        self.running = True
        log.info("initialization complete")
    
    def _empty_random_position(self):
        """ returns a (x,y) position on the board that is empty ( value = 0 ) """
        empty_positions = np.argwhere(self.board == 0) 
        return empty_positions[np.random.randint(0, len(empty_positions))]
    
    def _add_food(self):
        """ adds a food to a random empty position on the board """
        x, y = self._empty_random_position()
        self.board[x, y] = FRUIT_TILE

   
