from structures.graph import Graph


# available positions (195) on world map (Tuple with x and y)
# i - row number, j - position in row number (column number)
class World:
    def __init__(self, game):
        self.game = game
        self.size = len(self.game.POSITIONS[:]), len(self.game.POSITIONS[0][:])
        self.G = Graph()
        self.build_graph()

    # map size: n x m (rows x columns)
    def build_graph(self):
        n, m = self.size
        # first graph G with only vertices (i, j)
        for i in range(n):
            for j in range(m):
                self.G.add_vertex((i, j))
        # next every vertex gets all possible neighbours
        for v in self.G:
            v_i, v_j = v.id
            self.G.add_edge((v_i, v_j), (v_i, v_j), cost=0)
            if v_j + 1 <= 14:
                self.G.add_edge((v_i, v_j), (v_i, v_j + 1))
                if v_i % 2 != 0:
                    if v_i - 1 >= 0:
                        self.G.add_edge((v_i, v_j), (v_i - 1, v_j + 1))
                    if v_i + 1 <= 12:
                        self.G.add_edge((v_i, v_j), (v_i + 1, v_j + 1))
            if v_j - 1 >= 0:
                self.G.add_edge((v_i, v_j), (v_i, v_j - 1))
                if v_i % 2 == 0:
                    if v_i - 1 >= 0:
                        self.G.add_edge((v_i, v_j), (v_i - 1, v_j - 1))
                    if v_i + 1 <= 12:
                        self.G.add_edge((v_i, v_j), (v_i + 1, v_j - 1))
            if v_i + 1 <= 12:
                self.G.add_edge((v_i, v_j), (v_i + 1, v_j))
            if v_i - 1 >= 0:
                self.G.add_edge((v_i, v_j), (v_i - 1, v_j))
