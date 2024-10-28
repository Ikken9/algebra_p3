import pygame
import sys
import os
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = random.choice([
            (255, 0, 0),    # Rojo
            (0, 255, 0),    # Verde
            (0, 0, 255),    # Azul
            (255, 255, 0),  # Amarillo
            (255, 0, 255),  # Magenta
            (0, 255, 255)   # Cian
        ])
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.randint(30, 60)  # Frames que vivirá la partícula

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class GameUI:
    def __init__(self, screen, clock, screen_width, screen_height, font, grid_size, game):
        self.screen = screen
        self.clock = clock
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.grid_size = grid_size
        self.game = game

        # Dimensiones y configuración
        self.GRID_MARGIN = 50
        self.LABEL_MARGIN = 30  # Nuevo margen para las etiquetas de filas y columnas
        self.BUTTON_SIZE = 40
        self.FPS = 30

        # Posición de inicio del tablero ajustada para acomodar las etiquetas
        self.grid_x = self.GRID_MARGIN + self.LABEL_MARGIN
        self.grid_y = self.GRID_MARGIN + self.LABEL_MARGIN

        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (230, 230, 230)
        self.BLUE = (0, 0, 255)

        # Preparar botones del grid sin espacios entre ellos
        self.buttons = []
        for row in range(self.grid_size):
            button_row = []
            for col in range(self.grid_size):
                rect = pygame.Rect(
                    self.grid_x + col * self.BUTTON_SIZE,  # Sin espacio entre celdas
                    self.grid_y + row * self.BUTTON_SIZE,  # Sin espacio entre celdas
                    self.BUTTON_SIZE,
                    self.BUTTON_SIZE
                )
                button_row.append(rect)
            self.buttons.append(button_row)

        # Obtener pasos de solución
        solution_steps = self.game.get_solution_positions()
        if solution_steps is not None:
            self.step_texts = [f"Paso {idx}: Presiona la posición ({r + 1}, {c + 1})" for idx, (r, c) in enumerate(solution_steps, 1)]
        else:
            self.step_texts = ["No hay solución disponible."]

        # Variables de scroll
        self.scroll_y = 0
        self.step_height = 30  # Altura de cada paso
        self.text_area_height = self.screen_height - 2 * self.GRID_MARGIN - 50  # Ajustar según diseño
        self.max_scroll = max(0, len(self.step_texts) * self.step_height - self.text_area_height)

        # Cargar la imagen de felicitación
        # Asegúrate de que la imagen 'felicidades.png' esté en el mismo directorio que este script
        try:
            image_path = os.path.join(os.path.dirname(__file__), 'ganaste.png')
            self.felicidades_image = pygame.image.load(image_path).convert_alpha()
            # Escalar la imagen si es necesario
            self.felicidades_image = pygame.transform.scale(self.felicidades_image, (300, 300))  # Ajusta el tamaño según sea necesario
        except pygame.error as e:
            print(f"Error al cargar la imagen de felicitación: {e}")
            self.felicidades_image = None

    def draw_column_labels(self):
        for col in range(self.grid_size):
            label = self.font.render(str(col + 1), True, self.BLACK)
            label_rect = label.get_rect(
                center=(
                    self.grid_x + col * self.BUTTON_SIZE + self.BUTTON_SIZE / 2,
                    self.GRID_MARGIN + self.LABEL_MARGIN / 2
                )
            )
            self.screen.blit(label, label_rect)

    def draw_row_labels(self):
        for row in range(self.grid_size):
            label = self.font.render(str(row + 1), True, self.BLACK)
            label_rect = label.get_rect(
                center=(
                    self.GRID_MARGIN + self.LABEL_MARGIN / 2,
                    self.grid_y + row * self.BUTTON_SIZE + self.BUTTON_SIZE / 2
                )
            )
            self.screen.blit(label, label_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Detectar clic en los botones del grid
                    for row in range(self.grid_size):
                        for col in range(self.grid_size):
                            if self.buttons[row][col].collidepoint(mouse_x, mouse_y):
                                self.game.toggle(row, col)
                                if self.game.is_solved():
                                    self.show_victory_message()
                                break

                    # Manejo del scroll
                    if event.button == 4:  # Scroll arriba
                        self.scroll_y = max(self.scroll_y - 30, 0)
                    elif event.button == 5:  # Scroll abajo
                        self.scroll_y = min(self.scroll_y + 30, self.max_scroll)

            self.screen.fill(self.WHITE)

            # Dibujar etiquetas de filas y columnas
            self.draw_column_labels()
            self.draw_row_labels()

            # Dibujar el tablero de juego sin espacios entre celdas
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rect = self.buttons[row][col]
                    color = self.GREEN if self.game.grid[row][col] == 1 else self.RED
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)  # Borde más delgado para mejor apariencia

            # Dibujar los pasos de la solución
            solution_frame = pygame.Rect(
                self.grid_x + self.grid_size * self.BUTTON_SIZE + 20,  # Ajuste para dejar espacio entre el tablero y la lista
                self.grid_y,
                self.screen_width - (self.grid_x + self.grid_size * self.BUTTON_SIZE + 3 * self.GRID_MARGIN),
                self.screen_height - 2 * self.GRID_MARGIN
            )
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, solution_frame)
            pygame.draw.rect(self.screen, self.BLACK, solution_frame, 2)

            # Título de la solución
            solution_title = self.font.render("Pasos para resolver el juego:", True, self.BLACK)
            self.screen.blit(solution_title, (solution_frame.x + 10, solution_frame.y + 10))

            # Área de texto con scroll utilizando una superficie recortada para evitar desbordes
            text_area = pygame.Rect(solution_frame.x + 10, solution_frame.y + 40, solution_frame.width - 20, solution_frame.height - 50)
            pygame.draw.rect(self.screen, self.WHITE, text_area)
            pygame.draw.rect(self.screen, self.BLACK, text_area, 1)

            # Crear una superficie para el área de texto con el tamaño exacto
            text_surface = pygame.Surface((text_area.width - 10, text_area.height))
            text_surface.set_colorkey(self.WHITE)  # Hacer transparente el fondo si es necesario
            text_surface.fill(self.WHITE)

            # Renderizar los pasos en la superficie de texto
            y_offset = -self.scroll_y
            for text in self.step_texts:
                text_render = self.font.render(text, True, self.BLACK)
                text_surface.blit(text_render, (0, y_offset))
                y_offset += self.step_height

            # Dibujar la superficie de texto en el área de texto utilizando el rectángulo de destino
            self.screen.blit(text_surface, (text_area.x + 5, text_area.y), area=pygame.Rect(0, 0, text_area.width - 10, text_area.height))

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def show_victory_message(self):
        # Mensaje actualizado
        message = "¡Felicidades, has completado el juego!"
        particles = []  # Lista para almacenar partículas de confeti
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False  # Cerrar el mensaje al hacer clic

            # Dibujar fondo semitransparente
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Transparencia
            self.screen.blit(overlay, (0, 0))

            # Añadir nuevas partículas de confeti
            for _ in range(5):  # Número de partículas por frame
                x = random.randint(0, self.screen_width)
                y = random.randint(0, self.screen_height)
                particles.append(Particle(x, y))

            # Actualizar y dibujar partículas
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)
                else:
                    particle.draw(self.screen)

            # Dibujar la imagen de felicitación si está cargada
            if self.felicidades_image:
                image_rect = self.felicidades_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
                self.screen.blit(self.felicidades_image, image_rect)

            # Dibujar el mensaje
            message_surface = self.font.render(message, True, self.WHITE)
            message_rect = message_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))
            self.screen.blit(message_surface, message_rect)

            pygame.display.flip()
            self.clock.tick(self.FPS)

