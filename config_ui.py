import pygame
import sys

class ConfigUI:
    def __init__(self, screen, clock, screen_width, screen_height, font):
        self.screen = screen
        self.clock = clock
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.grid_size = 5  # Valor inicial

        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.BLUE = (0, 0, 255)
        self.RED = (200, 0, 0)
        self.GREEN = (0, 200, 0)  # Nuevo color para el botón de sumar

        # Definir botones (se actualizarán en cada ciclo de renderizado)
        self.decrease_button = pygame.Rect(0, 0, 50, 50)
        self.increase_button = pygame.Rect(0, 0, 50, 50)
        self.start_button = pygame.Rect(0, 0, 150, 50)

    def run(self):
        selecting = True

        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Detectar clic en los botones
                    if self.decrease_button.collidepoint(mouse_x, mouse_y):
                        self.grid_size = max(self.grid_size - 1, 2)
                    elif self.increase_button.collidepoint(mouse_x, mouse_y):
                        self.grid_size = min(self.grid_size + 1, 20)
                    elif self.start_button.collidepoint(mouse_x, mouse_y):
                        return self.grid_size

            self.screen.fill(self.WHITE)

            # Título
            title_text = "Selecciona el Tamaño del Grid (2x2 a 20x20):"
            title_surface = self.font.render(title_text, True, self.BLACK)
            self.screen.blit(
                title_surface,
                (
                    self.screen_width // 2 - title_surface.get_width() // 2,
                    self.screen_height // 2 - 150,
                ),
            )

            # Botón disminuir (Rojo)
            self.decrease_button = pygame.Rect(
                self.screen_width // 2 - 80, self.screen_height // 2 - 25, 50, 50
            )
            pygame.draw.rect(self.screen, self.RED, self.decrease_button)
            minus_text = self.font.render("-", True, self.WHITE)
            minus_rect = minus_text.get_rect(center=self.decrease_button.center)
            self.screen.blit(minus_text, minus_rect)

            # Tamaño actual
            size_text = self.font.render(f"{self.grid_size} x {self.grid_size}", True, self.BLACK)
            self.screen.blit(
                size_text,
                (
                    self.screen_width // 2 - size_text.get_width() // 2,
                    self.screen_height // 2,
                ),
            )

            # Botón aumentar (Verde)
            self.increase_button = pygame.Rect(
                self.screen_width // 2 + 30, self.screen_height // 2 - 25, 50, 50
            )
            pygame.draw.rect(self.screen, self.GREEN, self.increase_button)
            plus_text = self.font.render("+", True, self.WHITE)
            plus_rect = plus_text.get_rect(center=self.increase_button.center)
            self.screen.blit(plus_text, plus_rect)

            # Botón iniciar juego
            self.start_button = pygame.Rect(
                self.screen_width // 2 - 75, self.screen_height // 2 + 50, 150, 50
            )
            pygame.draw.rect(self.screen, self.BLUE, self.start_button)
            start_text = self.font.render("Iniciar Juego", True, self.WHITE)
            start_rect = start_text.get_rect(center=self.start_button.center)
            self.screen.blit(start_text, start_rect)

            pygame.display.flip()
            self.clock.tick(30)
