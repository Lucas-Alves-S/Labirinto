import time
import os
import threading
from random import randrange

class Maze:
    """This is a primary object meant to hold a rectangular, 2D maze."""

    def __init__(self, seed=None):
        self.generator = None
        self.grid = None
        self.starts = []
        self.end = None
        self.transmuters = []
        self.solver = None
        self.solutions = None
        self.prune = True
        self.paths = {start: [] for start in self.starts}
        self.lock = threading.Lock()
        self.max_steps = 0
        self.stop_animation = False
        self.current_positions = None
        Maze.set_seed(seed)

    @staticmethod
    def set_seed(seed):
        """Set the random seeds for random libraries."""
        if seed is not None:
            import random

            random.seed(seed)
            import numpy as np

            np.random.seed(seed)

    def generate(self):
        """Generate a new maze and handle clean-up."""
        assert not (self.generator is None), "No maze-generation algorithm has been set."

        self.grid = self.generator.generate()
        self.starts = []
        self.end = None
        self.solutions = None

    def generate_entrances(self, num_entrances=3, start_outer=True):
        """Generate maze entrances, allowing multiple entries."""
        for _ in range(num_entrances):
            if start_outer:
                start = self._generate_outer_entrance()
            else:
                start = self._generate_inner_entrance()
            self.starts.append(start)
        
        self.end = (0,1) # Final fixo igual o professor pediu
        self.current_positions = {start: 0 for start in self.starts}  # Para pegar a posição de cada rato

    def _generate_outer_entrance(self):
        """Generate an outer entrance on the walls of the maze."""
        H = self.grid.shape[0]
        W = self.grid.shape[1]
        side = randrange(4)

        if side == 0:  # North
            return (0, randrange(1, W, 2))
        elif side == 1:  # South
            return (H - 1, randrange(1, W, 2))
        elif side == 2:  # West
            return (randrange(1, H, 2), 0)
        else:  # East
            return (randrange(1, H, 2), W - 1)

    def _generate_inner_entrance(self):
        """Generate a random inner entrance within the maze."""
        H, W = self.grid.shape
        return (randrange(1, H, 2), randrange(1, W, 2))

    def solve(self):
        """Resolve o labirinto e retorna uma solução (se houver)."""
        assert not (self.solver is None), "No maze-solving algorithm has been set."
        assert self.end is not None, "End must be set first."

        self.solutions = []
        for start in self.starts:
            solution = self.solver.solve(self.grid, start, self.end)
            if self.prune:
                solution = self.solver.prune_solutions(solution)
            self.solutions.extend(solution)

    def calculate_paths(self):
        for start in self.starts:
            current_position = list(start)
            path = self.solver.solve(self.grid, tuple(current_position), self.end)
            if path and path[0]:
                self.paths[start] = path[0]
                self.max_steps = max(self.max_steps, len(path[0]))
            else:
                print(f"Nenhum caminho encontrado para {start}.")
                self.paths[start] = []

    def animate_rato(self, start):
        path = self.paths[start]
        for step_index in range(len(path)):
            if self.stop_animation:
                break
            
            time.sleep(0.2)  # Tempo de movimento do rato
            with self.lock:
                if step_index < len(path):
                    self.current_positions[start] = step_index  # Atualiza a posição atual do rato

    def render(self):
        while not self.stop_animation:
            os.system('cls' if os.name == 'nt' else 'clear')

            display_grid = []
            for r in range(len(self.grid)):
                row = "".join(["⬜" if cell else "⬛" for cell in self.grid[r]])

                # Atualiza a posição de todos os ratos
                with self.lock:
                    for start in self.starts:
                        step_index = self.current_positions[start]
                        path = self.paths[start]
                        if step_index < len(path):
                            current_position = path[step_index]
                            if (r, current_position[1]) == (current_position[0], current_position[1]):
                                row = row[:current_position[1]] + "🐀" + row[current_position[1] + 1:]

                # Mostra o Queijo
                if (r, self.end[1]) == (self.end[0], self.end[1]):
                    row = row[:self.end[1]] + "🧀" + row[self.end[1]:]

                display_grid.append(row)

            print("\n".join(display_grid))
            time.sleep(0.2)  # Controla a taxa de atualização da tela (FPS omg)

    def animate(self):
        self.calculate_paths()
        render_thread = threading.Thread(target=self.render)
        render_thread.start()

        # Inicia threads para cada rato
        threads = []
        for start in self.starts:
            thread = threading.Thread(target=self.animate_rato, args=(start,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.stop_animation = True
        render_thread.join()

    def tostring(self, entrances=False, solutions=False):
        """Return a string representation of the maze."""
        if self.grid is None:
            return ""

        txt = []
        for row in self.grid:
            txt.append("".join(["#" if cell else " " for cell in row]))

        if entrances and self.starts and self.end:
            for r, c in self.starts:
                txt[r] = txt[r][:c] + "R" + txt[r][c + 1 :]
            r, c = self.end
            txt[r] = txt[r][:c] + "Q" + txt[r][c + 1 :]

        if solutions and self.solutions:
            for path in self.solutions:
                for r, c in path:
                    txt[r] = txt[r][:c] + "+" + txt[r][c + 1 :]

        return "\n".join(txt)

    def __str__(self):
        """Display maze walls, entrances, and solutions, if available."""
        return self.tostring(True, True)

    def __repr__(self):
        """Display maze walls, entrances, and solutions, if available."""
        return self.__str__()
