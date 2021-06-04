from structures.min_heap import MinHeap
from structures.bfs import BFS
from math import inf


class Dijkstra(BFS):
    def clear(self):
        super().clear()
        for v_key in self.g.vert_list:
            self.distances[v_key] = inf

    def dijkstra(self, start_key):
        self.clear()
        self.distances[start_key] = 0
        h = MinHeap((v, k) for k, v in self.distances.items())

        while not h.is_empty():
            current_distance, cur_key = h.extract_min()
            if current_distance == inf:
                return

            current_vert = self.g.get_vertex(cur_key)
            self.distances[cur_key] = current_distance
            self.colors[cur_key] = 'black'
            for nbr in current_vert.get_connections():
                nbr_key = nbr.get_id()
                if self.colors[nbr_key] != 'white':
                    continue
                weight = current_vert.get_weight(nbr)
                neighbor_distance = self.distances[nbr_key]
                if current_distance + weight < neighbor_distance:
                    h.decrease_key((neighbor_distance, nbr_key),
                                   (current_distance + weight, nbr_key))
                    self.distances[nbr_key] = current_distance + weight
                    self.predecessors[nbr_key] = current_vert
