"""
Simulator of graphons

Reference:
Chan, Stanley, and Edoardo Airoldi.
"A consistent histogram estimator for exchangeable graph models."
In International Conference on Machine Learning, pp. 208-216. 2014.
"""

import numpy as np
from typing import List


def synthesize_graphon(r: int=1000, type_idx: int=0) -> np.ndarray:
    """
    Synthesize graphons
    :param r: the resolution of discretized graphon
    :param type_idx: the type of graphon
    :return:
        w: (r, r) float array, whose element is in the range [0, 1]
    """
    u = ((np.arange(0, r) + 1) / r).reshape(-1, 1)  # (r, 1)
    u = u[::-1, :]
    v = ((np.arange(0, r) + 1) / r).reshape(1, -1)  # (1, r)
    v = v[:, ::-1]
    if type_idx == 0:
        w = u @ v
    elif type_idx == 1:
        w = np.exp(-(u ** 0.7 + v ** 0.7))
    elif type_idx == 2:
        w = 0.25 * (u ** 2 + v ** 2 + u ** 0.5 + v ** 0.5)
    elif type_idx == 3:
        w = 0.5 * (u + v)
    elif type_idx == 4:
        w = 1 / (1 + np.exp(-10 * (u ** 2 + v ** 2)))
    elif type_idx == 5:
        w = np.abs(u - v)
    elif type_idx == 6:
        w = 1 / (1 + np.exp(-(np.maximum(u, v) ** 2 + np.minimum(u, v) ** 4)))
    elif type_idx == 7:
        w = np.exp(-np.maximum(u, v) ** 0.75)
    elif type_idx == 8:
        w = np.exp(-0.5 * (np.minimum(u, v) + u ** 0.5 + v ** 0.5))
    elif type_idx == 9:
        w = np.log(1 + 0.5 * np.maximum(u, v))
    else:
        w = u @ v
    return w


def simulate_graphs(w: np.ndarray, num_graphs: int=10, num_nodes: int=200, graph_size: str='fixed') -> List[np.ndarray]:
    """
    Simulate graphs based on a graphon
    :param w: a (r, r) discretized graphon
    :param num_graphs: the number of simulated graphs
    :param num_nodes: the number of nodes per graph
    :param graph_size: fix each graph size as num_nodes or sample the size randomly as num_nodes * (0.5 + uniform)
    :return:
        graphs: a list of binary adjacency matrices
    """
    graphs = []
    r = w.shape[0]
    if graph_size == 'fixed':
        numbers = [num_nodes for _ in range(num_graphs)]
    elif graph_size == 'random':
        numbers = [int(num_nodes * (0.5 + np.random.rand())) for _ in range(num_graphs)]
    else:
        numbers = [num_nodes for _ in range(num_graphs)]
    print(numbers)

    for n in range(num_graphs):
        node_locs = (r * np.random.rand(numbers[n])).astype('int')
        graph = w[node_locs, :]
        graph = graph[:, node_locs]
        noise = np.random.rand(graph.shape[0], graph.shape[1])
        graph -= noise
        graphs.append((graph > 0).astype('float'))

    return graphs


def mean_square_error(graphon, estimation):
    return np.linalg.norm(graphon - estimation)


def relative_error(graphon, estimation):
    return np.linalg.norm(graphon - estimation) / np.linalg.norm(graphon)

# # test
# graphon = synthetic_graphon(r=1000, type_idx=1)
# graphs = simulate_graphs(w=graphon, num_graphs=10, num_nodes=200, graph_size='random')
# print(graphs.keys())
