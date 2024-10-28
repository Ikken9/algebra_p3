import numpy as np

class LightsOutGame:
    def __init__(self, size):
        self.size = size
        self.grid = np.random.randint(2, size=(size, size))
        while self.get_solution_positions() is None:
            self.grid = np.random.randint(2, size=(size, size))

    def toggle(self, row, col):
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.grid[nr][nc] = 1 - self.grid[nr][nc]

    def is_solved(self):
        return np.all(self.grid == 0)

    def solve(self):
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

        A = A % 2
        b = b % 2
        solution = self.gaussian_elimination(A, b)
        if solution is None:
            return None
        return solution.reshape((n, n))

    def gaussian_elimination(self, A, b):
        n = len(b)
        for col in range(n):
            pivot_row = None
            for row in range(col, n):
                if A[row, col] == 1:
                    pivot_row = row
                    break

            if pivot_row is None:
                continue

            A[[col, pivot_row]] = A[[pivot_row, col]]
            b[[col, pivot_row]] = b[[pivot_row, col]]

            for row in range(col + 1, n):
                if A[row, col] == 1:
                    A[row] = (A[row] + A[col]) % 2
                    b[row] = (b[row] + b[col]) % 2

        for row in range(n):
            if np.all(A[row] == 0) and b[row] == 1:
                return None

        x = np.zeros(n, dtype=int)
        for row in range(n - 1, -1, -1):
            if A[row, row] == 1:
                x[row] = b[row]
                for col in range(row + 1, n):
                    x[row] = (x[row] - A[row, col] * x[col]) % 2

        return x

    def get_solution_positions(self):
        solution_matrix = self.solve()
        if solution_matrix is None:
            return None
        positions = [(i, j) for i in range(self.size) for j in range(self.size) if solution_matrix[i, j] == 1]
        return positions

    def apply_solution(self):
        solution_positions = self.get_solution_positions()
        if solution_positions is None:
            return
        for row, col in solution_positions:
            self.toggle(row, col)
