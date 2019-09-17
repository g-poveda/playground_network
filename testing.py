import maze
import bfs
import dfs
import time
import networkx as nx
import numpy as np


def create_mazes():
    import pickle
    for size in np.arange(2000, 5001, 100):
        print(size)
        t = time.time()
        maze_, graph = maze.do_maze(size, 
                                    size)
        pickle.dump(graph, open("mazes/graph_"+str(size)+".pk", 'wb'))
        t_end = time.time()
        print(t_end-t, " sec ")


def testing():
    t = time.time()
    #maze_, graph = maze.do_maze(300, 300)
    import pandas as pd
    import pickle
    #pickle.dump(graph, open("graph_300.pk", 'wb'))
    graph = pickle.load(open('mazes/graph_2000.pk', 'rb'))
    print(time.time()-t, " to build maze ")
    g = nx.DiGraph()
    g.add_nodes_from(list(graph.keys()))
    g.add_edges_from([(k, s)  for k in graph for s in graph[k]])
    keys = list(graph.keys())
    start = min(keys, key=lambda x: abs(x[0])+abs(x[1]))
    end = max(keys, key=lambda x: abs(x[0]-start[0])+abs(x[1]-start[0]))
    print(start, end)
    t = time.time()
    p = nx.astar_path(g, start, end,
                      heuristic=lambda x,y: abs(x[0]-y[0])+abs(x[1]-y[1]))
    # print(p)
    print(time.time()-t, " sec for A*")
    t = time.time()
    p = nx.dijkstra_path(g, start, end)
    # print(p)
    print(time.time()-t, " sec for dijkstra")
    dfs_p = dfs.dfs_paths_1(graph, start=start, goal=end)
    bfs_p = bfs.bfs_paths(graph, start=start, goal=end)
    t = time.time()
    d = next(dfs_p)
    print(time.time()-t, ' sec for dfs')
    t = time.time()
    b = next(bfs_p)
    print(time.time()-t, ' sec for bfs')

    
if __name__ == "__main__":
    #create_mazes()
    #create_mazes()
    testing()