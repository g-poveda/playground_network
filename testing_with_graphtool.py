import maze
import bfs
import dfs
import time
from graph_tool.all import *
import numpy as np
class VisitorExample(AStarVisitor):
    def __init__(self, touched_v,
                 touched_e,
                 target):
        self.touched_v = touched_v
        self.touched_e = touched_e
        self.target = target

    def discover_vertex(self, u):
        self.touched_v[u] = True

    def examine_edge(self, e):
        self.touched_e[e] = True

    def edge_relaxed(self, e):
        if e.target() == self.target:
            print(e.target(), self.target)
            raise StopSearch()

def testing():
    t = time.time()
    maze_, graph = maze.do_maze(1000, 1000)
    import pickle
    #graph = pickle.load(open("mazes/graph_100.pk", 'rb'))
    edges = [(k, s) for k in graph for s in graph[k]]
    print(time.time()-t, " to build maze ")
    g = Graph()
    dict_vertex = {k: k
                   for k in graph}
    keys_ = list(dict_vertex.keys())
    index_to_key = {keys_[i]: i for i in range(len(keys_))}
    start = min(keys_, key=lambda x: abs(x[0])+abs(x[1]))
    end = max(keys_, key=lambda x: abs(x[0]-start[0])+abs(x[1]-start[0]))
    print(start, end)
    g.add_vertex(len(keys_))
    n = g.num_vertices()
    coordinates = g.new_vertex_property("vector<float>")
    id_ = g.new_vertex_property("string")
    distances = g.new_edge_property("float")
    for i in range(n):
        coordinates[g.vertex(i)] = [dict_vertex[keys_[i]][0],
                                    dict_vertex[keys_[i]][1]]
        id_[i] = keys_[i]
    for edge in edges:
        c1 = g.vertex(index_to_key[edge[0]])
        c2 = g.vertex(index_to_key[edge[1]])
        e = g.add_edge(c1,
                       c2)
        distances[e] = 1
        #distances[e] = abs(coordinates[c1][0]-coordinates[c2][0])
        #+abs(coordinates[c1][1]-coordinates[c2][1])
    def heuristic(current, target, coordinates):
        return (np.abs(coordinates[current][0]-coordinates[target][0])
                +np.abs(coordinates[current][1]-coordinates[target][1]))
    print("graph setup")
    touch_v = g.new_vertex_property("bool")
    touch_e = g.new_edge_property("bool")
    t = time.time()
    dist, pred = astar_search(g, source=g.vertex(index_to_key[start]),
                              weight=distances,
                              visitor=VisitorExample(touch_v,
                                                     touch_e,
                                                     g.vertex(index_to_key[end])),
                              heuristic=lambda v: heuristic(v, 
                              g.vertex(index_to_key[end]), 
                              coordinates))
    t_end =time.time()
    print(t_end-t, " sec")
    ecolor = g.new_edge_property("string")
    ewidth = g.new_edge_property("double")
    ewidth.a = 0.5
    for e in g.edges():
       ecolor[e] = "#3465a4" if touch_e[e] else "#d3d7cf"
    v = g.vertex(index_to_key[end])
    while v != g.vertex(index_to_key[start]):
        p = g.vertex(pred[v])
        for e in v.in_edges():
            if e.source() == p:
                ecolor[e] = "#a40000"
                ewidth[e] = 2
        v = p
    import matplotlib
    import matplotlib.pyplot as plt
    
    graph_draw(g,
               pos=coordinates,
               vcmap=matplotlib.cm.binary,
               output_size=(4000, 4000),
               vertex_fill_color=touch_v,
               edge_color=ecolor,
               edge_pen_width=ewidth,
               output="astar-delaunay.png")
    

    
if __name__ == "__main__":
    testing()