import os

if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hidden'
    print("######## SnakeGame ########", end="\n")
    
    import src.snake as snake
    snake_game = snake.Game()
    snake_game.run()