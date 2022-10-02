import src.logger as logger
from src.constants import TILE, COLOR, tile_to_color, flip_background_color
from typing import Sequence, Tuple
import logging as log
import numpy as np
import pygame

class Game:
    def __init__(self, board_size=32, headless=False):
        self.width = 800
        self.height = 800
        self.headless = headless
        self.running = False
        self.screen = None
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=np.int8)
        self.snake_size = 1
        self.window_title = "Snake Game"
        self.score = 0
        self.fps = 10
        self.clock = None

        # make the walls
        self.board[0, :] = TILE.WALL
        self.board[:, 0] = TILE.WALL
        self.board[board_size - 1, :] = TILE.WALL
        self.board[:, board_size - 1] = TILE.WALL

        self.board[6, board_size // 2] = 1  # add snake on the board
        self.__add_food()

        self.grid_step = self.width // self.board_size

    def run(self):
        """ main game loop """
        self.__initialize()
        while self.running:
            for event in pygame.event.get():
                self.__handle_event(event)
            self.__draw()
            self.__handle_input()
        pygame.quit()

    def __handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        """ handle user input """
        if pressed_keys[pygame.K_LEFT]:
            self.__move_snake((-1, 0))
        elif pressed_keys[pygame.K_RIGHT]:
            self.__move_snake((1, 0))
        elif pressed_keys[pygame.K_UP]:
            self.__move_snake((0, -1))
        elif pressed_keys[pygame.K_DOWN]:
            self.__move_snake((0, 1))

    def __handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False

    def __draw(self):
        if self.headless:
            return
        self.__draw_board()
        self.__draw_score()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def __draw_board(self):
        for x in range(self.board_size):
            flip_background_color()
            for y in range(self.board_size):
                x_pos = self.grid_step * x
                y_pos = self.grid_step * y

                tile_color = tile_to_color(self.board[x, y])
                flip_background_color()
                pygame.draw.rect(self.screen, tile_color, [x_pos, y_pos, self.grid_step, self.grid_step])
    
    def __draw_score(self):
        font = pygame.font.Font(None, 30)
        text = font.render("score: " + str(self.score), 1, COLOR.WHITE)
        self.screen.blit(text, (10, 2))

    def __initialize(self):
        """ basic initialization for the game window and pygame itself """
        logger.config_log()
        log.info("initializing snake game")
        pygame.init()

        if not self.headless:
            self.screen = pygame.display.set_mode([self.width, self.height])
            self.clock = pygame.time.Clock()
            pygame.display.set_caption("Snake")
            log.info("screen dimensions set to %s", self.screen.get_size())
        else:
            log.info("headless mode enabled")

        self.running = True
        log.info("initialization complete")

    def __empty_random_position(self):
        """ returns a (x,y) position on the board that is empty ( value = 0 ) """
        empty_positions = np.argwhere(self.board == 0)
        return empty_positions[np.random.randint(0, len(empty_positions))]

    def __add_food(self):
        """ adds a food to a random empty position on the board """
        x, y = self.__empty_random_position()
        self.board[x, y] = TILE.FRUIT
    
    def __add_wall(self):
        """ adds a wall in a random empty position on the board """
        x, y = self.__empty_random_position()
        self.board[x, y] = TILE.WALL
    
    def __move_snake(self, direction: Tuple[int, int]):
        """ moves the snake in the given direction """
        head_x, head_y = np.argwhere(self.board == 1)[0]
        self.board[head_x, head_y] = 0
        x,y = head_x + direction[0], head_y + direction[1]
        self.__process_board(x,y)
        self.board[x, y] = 1
    
    def __handle_snake_growth(self):
        """ add a snake_size +1 to the board representing the new snake body"""
        pass

    
    def __process_board(self, x, y):
        """ processes the board and checks for collisions and food """
        if self.board[x, y] == TILE.FRUIT:
            self.__add_food()
            self.__add_wall()
            self.score += 1
        elif self.board[x, y] == TILE.WALL:
            self.running = False