import tkinter as tk
from ui import LightsOutApp

def start_game(size):
    # Inicia el juego con el tamaño de grid especificado
    root = tk.Tk()
    root.title(f"Lights Out - {size}x{size}")
    app = LightsOutApp(root, size)
    root.mainloop()

def select_grid_size():
    # Interfaz para seleccionar el tamaño del grid
    root = tk.Tk()
    root.title("Seleccionar Tamaño del Grid")
    label = tk.Label(root, text="Selecciona el Tamaño del Grid (2x2 a 20x20):")
    label.pack(pady=10)

    size_var = tk.IntVar(value=5)
    size_slider = tk.Scale(root, from_=2, to=20, orient="horizontal", variable=size_var)
    size_slider.pack(pady=10)

    start_button = tk.Button(root, text="Iniciar Juego", command=lambda: [root.destroy(), start_game(size_var.get())])
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    select_grid_size()