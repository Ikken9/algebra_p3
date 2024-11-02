import pygame
import sys
from config_ui import ConfigUI
from game_ui import GameUI
from game_logic import LightsOutGame

def main():
    # Configuración de Pygame
    pygame.init()

    # Dimensiones de la pantalla
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lights Out")

    clock = pygame.time.Clock()

    # Configuración de la fuente
    FONT = pygame.font.SysFont(None, 24)

    # Iniciar pantalla de configuración
    config_ui = ConfigUI(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, FONT)
    grid_size = config_ui.run()

    # Iniciar el juego con el tamaño de grid seleccionado
    game = LightsOutGame(grid_size)
    game_ui = GameUI(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, FONT, grid_size, game)
    game_ui.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


