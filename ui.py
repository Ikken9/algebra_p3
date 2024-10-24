import tkinter as tk
from tkinter import scrolledtext
from game_logic import LightsOutGame

class LightsOutApp:
    def __init__(self, root, size):
        # Inicializa la interfaz de usuario del juego
        self.root = root
        self.size = size
        self.game = LightsOutGame(size)

        self.main_frame = tk.Frame(root, width=1000, height=500)
        self.main_frame.pack()

        # Configuración del tablero a la izquierda
        self.board_frame = tk.Frame(self.main_frame, width=500, height=500)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        # Crear los números de las columnas en la parte superior
        for col in range(size):
            label = tk.Label(self.board_frame, text=str(col + 1), font=("Arial", 10))
            label.grid(row=0, column=col + 1)

        # Crear los números de las filas en la parte izquierda
        for row in range(size):
            label = tk.Label(self.board_frame, text=str(row + 1), font=("Arial", 10))
            label.grid(row=row + 1, column=0)

        # Crear los botones del tablero
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        for row in range(size):
            for col in range(size):
                button = tk.Button(self.board_frame, width=2, height=1, 
                                   bg="green" if self.game.grid[row][col] == 1 else "red",
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row + 1, column=col + 1, padx=0, pady=0)
                self.buttons[row][col] = button
        self.update_ui()
        
        # Configuración de los pasos para resolver a la derecha con un slide vertical
        self.solution_frame = tk.Frame(self.main_frame, width=500, height=500)
        self.solution_frame.grid(row=0, column=1, padx=10, pady=10)
        self.show_solution_steps()

    def on_button_click(self, row, col):
        # Maneja el evento cuando se presiona un botón del tablero
        self.game.toggle(row, col)
        self.update_ui()
        if self.game.is_solved():
            self.show_win_message()

    def update_ui(self):
        # Actualiza la interfaz de usuario del tablero
        for row in range(self.size):
            for col in range(self.size):
                color = "green" if self.game.grid[row][col] == 1 else "red"
                self.buttons[row][col].configure(bg=color)

    def show_win_message(self):
        # Muestra un mensaje de victoria cuando el tablero está resuelto
        win_message = tk.Label(self.root, text="¡Felicitaciones! ¡Has resuelto el puzzle!", font=("Arial", 14))
        win_message.pack(pady=10)

    def show_solution_steps(self):
        # Muestra los pasos para resolver el tablero
        solution_positions = self.game.get_solution_positions()
        if solution_positions is not None:
            step_text = "Pasos para resolver el juego:"
            step_label = tk.Label(self.solution_frame, text=step_text, font=("Arial", 12))
            step_label.pack(pady=5)

            text_area = scrolledtext.ScrolledText(self.solution_frame, width=40, height=20, wrap=tk.WORD)
            text_area.pack()
            for idx, (r, c) in enumerate(solution_positions, start=1):
                step = f"Paso {idx}: Presiona la posición ({r + 1}, {c + 1})\n"
                text_area.insert(tk.END, step)