import numpy as np

class LightsOutGame:
    def __init__(self, size):
        # Inicializa el tablero con un tamaño dado y genera un tablero aleatorio que tenga solución
        self.size = size
        self.grid = np.random.randint(2, size=(size, size))
        while self.get_solution_positions() is None:
            self.grid = np.random.randint(2, size=(size, size))

    def toggle(self, row, col):
        # Cambia el estado de la luz actual y de las luces adyacentes
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.grid[nr][nc] = 1 - self.grid[nr][nc]

    def is_solved(self):
        # Verifica si todas las luces están apagadas
        return np.all(self.grid == 0)

    def solve(self):
        # Representa el tablero como un sistema de ecuaciones lineales
        n = self.size
        A = np.zeros((n * n, n * n), dtype=int)
        b = self.grid.flatten()

        for i in range(n):
            for j in range(n):
                index = i * n + j
                A[index, index] = 1
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n:
                        neighbor_index = ni * n + nj
                        A[index, neighbor_index] = 1

        # Resolver el sistema en {0, 1} usando eliminación Gaussiana completa
        A = A % 2
        b = b % 2
        solution = self.gaussian_elimination(A, b)
        if solution is None:
            return None  # No hay solución
        return solution.reshape((n, n))

    def gaussian_elimination(self, A, b):
        # Aplica eliminación Gaussiana en el campo GF(2)
        n = len(b)
        for col in range(n):
            # Encontrar fila con un 1 en la columna actual
            pivot_row = None
            for row in range(col, n):
                if A[row, col] == 1:
                    pivot_row = row
                    break

            if pivot_row is None:
                continue  # No hay pivote en esta columna, pasar a la siguiente

            # Intercambiar filas
            A[[col, pivot_row]] = A[[pivot_row, col]]
            b[[col, pivot_row]] = b[[pivot_row, col]]

            # Eliminar el 1 de las filas inferiores
            for row in range(col + 1, n):
                if A[row, col] == 1:
                    A[row] = (A[row] + A[col]) % 2
                    b[row] = (b[row] + b[col]) % 2

        # Verificar si hay solución
        for row in range(n):
            if np.all(A[row] == 0) and b[row] == 1:
                return None  # No hay solución

        # Sustitución hacia atrás para encontrar la solución
        x = np.zeros(n, dtype=int)
        for row in range(n - 1, -1, -1):
            if A[row, row] == 1:
                x[row] = b[row]
                for col in range(row + 1, n):
                    x[row] = (x[row] - A[row, col] * x[col]) % 2

        return x

    def get_solution_positions(self):
        # Obtiene las posiciones que deben ser presionadas para resolver el tablero
        solution_matrix = self.solve()
        if solution_matrix is None:
            return None
        positions = [(i, j) for i in range(self.size) for j in range(self.size) if solution_matrix[i, j] == 1]
        return positions

    def apply_solution(self):
        # Aplica la solución al tablero si existe
        solution_positions = self.get_solution_positions()
        if solution_positions is None:
            return  # No hay solución
        for row, col in solution_positions:
            self.toggle(row, col)