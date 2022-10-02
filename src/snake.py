import src.logger as logger
from src.constants import TILE, COLOR, is_snake, tile_to_color
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
        self.window_title = "Snake"
        self.score = 0

        # make the walls
        self.board[0, :] = TILE.WALL
        self.board[:, 0] = TILE.WALL
        self.board[board_size - 1, :] = TILE.WALL
        self.board[:, board_size - 1] = TILE.WALL

        self.board[6, board_size // 2] = 1  # add snake on the board
        self._add_food()

        self.grid_step = self.width // self.board_size

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
        self.__draw_board()
        self.__draw_score()
        pygame.display.flip()

    def __draw_board(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                x_pos = self.grid_step * x
                y_pos = self.grid_step * y
                tile_color = tile_to_color(self.board[x, y])
                
                pygame.draw.rect(self.screen, tile_color, [x_pos, y_pos, self.grid_step, self.grid_step])
                # draw 1px border on the left and top if tile is EMPTY
                if self.board[x, y] == TILE.EMPTY:
                    pygame.draw.rect(self.screen, COLOR.LIGHT_GREY, [x_pos, y * self.grid_step, 1, self.grid_step])
                    pygame.draw.rect(self.screen, COLOR.LIGHT_GREY, [x_pos, y * self.grid_step, self.grid_step, 1])
    
    def __draw_score(self):
        font = pygame.font.Font(None, 30)
        text = font.render("score: " + str(self.score), 1, COLOR.LIGHT_BLUE)
        self.screen.blit(text, (10, 2))

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
        self.board[x, y] = TILE.FRUIT
