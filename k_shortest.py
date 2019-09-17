from heapq import heappush, heappop
from itertools import count
import networkx as nx


class Path:
    def __init__(self, list_node):
        self.list_node_tuple = tuple(list_node)
        self.list_node = list_node
        self.last = list_node[-1]

    def __eq__(self, other):
        return self.list_node_tuple == other.list_node_tuple

    def __hash__(self):
        return hash(self.list_node_tuple)


def k_shortest_path(G, sources,
                    target, weight,
                    k=1, 
                    k_lim=1,
                    heuristic=None,
                    max_relative_to_optimal_prune=2.,
                    min_relative_difference_prune=0.01,
                    max_relative_difference_prune=0.05,
                    min_absolute_difference_prune=3.,
                    max_absolute_difference_prune=200.):
    """
    Uses Dijkstra's algorithm to find shortest weighted paths

    Parameters
    ----------
    G : NetworkX graph

    sources : non-empty iterable of nodes
        Starting nodes for paths. If this is just an iterable containing
        a single node, then all paths computed by this function will
        start from that node. If there are two or more nodes in this
        iterable, the computed paths may begin from any one of the start
        nodes.

    weight: function
        Function with (u, v, data) input that returns that edges weight

    pred: dict of lists, optional(default=None)
        dict to store a list of predecessors keyed by that node
        If None, predecessors are not stored.

    paths: dict, optional (default=None)
        dict to store the path list from source to each node, keyed by node.
        If None, paths are not stored.

    target : node label, optional
        Ending node for path. Search is halted when target is found.

    cutoff : integer or float, optional
        Depth to stop the search. Only return paths with length <= cutoff.

    Returns
    -------
    distance : dictionary
        A mapping from node to shortest distance to that node from one
        of the source nodes.

    Raises
    ------
    NodeNotFound
        If any of `sources` is not in `G`.

    Notes
    -----
    The optional predecessor and path dictionaries can be accessed by
    the caller through the original pred and paths objects passed
    as arguments. No need to explicitly return pred or paths.

    """
    if heuristic is None:
        def _heuristic(x, y):
            return 0.
        heuristic = _heuristic
    G_succ = G._succ if G.is_directed() else G._adj
    push = heappush
    pop = heappop
    seen = {}
    # fringe is heapq with 3-tuples (heuristic, distance,counter,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []

    for source in sources:
        if source not in G:
            raise nx.NodeNotFound("Source {} not in G".format(source))
        seen[source] = [heuristic(source, target)]
        push(fringe, (heuristic(source, target), 0.,
                      next(c), Path([source])))
    count_path = {target: 0}
    results = {}
    map_path_open = {}
    map_path_closed = {}
    found_path = False
    best_cost = float('inf')
    while fringe and count_path[target] < k:
        (h, cc, _,  v) = pop(fringe)
        if v in map_path_closed:
            continue
        else:
            map_path_closed[v] = True
        last = v.last
        if last in count_path and count_path[last] <= k:
            count_path[last] += 1
        elif last not in count_path:
            count_path[last] = 1
        if last == target:
            results[count_path[last]] = (cc, v)
            print(count_path[last], "/", k)
            if not found_path:
                found_path = True
                best_cost = cc
            if count_path[last] == k:
                break
        if count_path[last] > k_lim:
            print("count path")
            continue
            # already searched this node.
        for u, e in G_succ[last].items():
            cost = weight(last, u, e)
            if cost is None:
                continue
            vu_dist = cc + cost
            wu_dist = vu_dist+heuristic(u, target)
            if found_path:
                if wu_dist >= (1+max_relative_to_optimal_prune)*best_cost:
                    continue
            if u not in seen or (u in count_path): # and count_path[u] <= k):
                if u in seen:
                    l = [abs(wu_dist-v)/max(v, 0.01)
                         for v in seen[u]]
                    if max(l) > max_relative_difference_prune:
                        continue
                    elif min(l) < min_relative_difference_prune:
                        continue
                    l = [abs(wu_dist - v)
                         for v in seen[u]]
                    if max(l) > max_absolute_difference_prune:

                        continue
                    elif min(l) < min_absolute_difference_prune:

                        continue
                else:
                    seen[u] = []
                path = Path(v.list_node+[u])
                if path in map_path_open:
                    continue
                seen[u] += [wu_dist]
                push(fringe, (wu_dist, vu_dist, next(c), path))
                map_path_open[path] = True
    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return results






