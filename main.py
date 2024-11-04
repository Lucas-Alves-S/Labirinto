from mazelib import Maze
from mazelib.generate.Wilsons import Wilsons # Escolher o algoritimo que gera o labirinto
from mazelib.solve.ShortestPath import ShortestPath # Escolher o algoritimo que resolver o labirinto

m = Maze()

m.generator = Wilsons(12,12) # tamanho, maior q 26x26 comeca a ficar meio paia
m.generate()
m.generate_entrances(num_entrances=5)

m.solver = ShortestPath()
m.solve()


m.animate()