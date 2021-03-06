import argparse
import numpy as np
import os
import pickle
import time
import methods.learner as learner
import methods.simulator as simulator


parser = argparse.ArgumentParser(description='Comparison for various methods on synthetic data')
parser.add_argument('--f-result', type=str,
                    default='results',
                    help='the root path saving learning results')
parser.add_argument('--r', type=int,
                    default=1000,
                    help='the resolution of graphon')
parser.add_argument('--num-graphs', type=int,
                    default=10,
                    help='the number of synthetic graphs')
parser.add_argument('--num-nodes', type=int, default=200,
                    help='the number of nodes per graph')
parser.add_argument('--graph-size', type=str, default='random',
                    help='the size of each graph, random or fixed')
parser.add_argument('--threshold-sba', type=float, default=0.1,
                    help='the threshold of sba method')
parser.add_argument('--threshold-usvt', type=float, default=0.1,
                    help='the threshold of usvt method')
parser.add_argument('--alpha', type=float, default=0.0003,
                    help='the weight of smoothness regularizer')
parser.add_argument('--beta', type=float, default=5e-3,
                    help='the weight of proximal term')
parser.add_argument('--gamma', type=float, default=0.1,
                    help='the weight of gw term')
parser.add_argument('--inner-iters', type=int, default=50,
                    help='the number of inner iterations')
parser.add_argument('--outer-iters', type=int, default=20,
                    help='the number of outer iterations')
parser.add_argument('--n-trials', type=int, default=1,
                    help='the number of trials')
args = parser.parse_args()


methods = ['SBA', 'SAS', 'LG', 'MC', 'USVT', 'GWB', 'SGWB', 'FGWB', 'SFGWB']

errors = np.zeros((13, len(methods), args.n_trials))
for i in range(13):
    graphon = simulator.synthesize_graphon(r=args.r, type_idx=i)
    simulator.visualize_graphon(graphon, save_path=os.path.join(args.f_result, 'graphon_{}.pdf'.format(i)))

    for n in range(args.n_trials):
        graphs = simulator.simulate_graphs(graphon,
                                           num_graphs=args.num_graphs,
                                           num_nodes=args.num_nodes,
                                           graph_size=args.graph_size)

        # simulator.visualize_unweighted_graph(graphs[0],
        #                                      save_path=os.path.join(args.f_result, 'adj_{}_{}.pdf'.format(i, n)))

        for m in range(len(methods)):
            since = time.time()
            _, estimation = learner.estimate_graphon(graphs, method=methods[m], args=args)
            simulator.visualize_graphon(estimation,
                                        title=methods[m],
                                        save_path=os.path.join(args.f_result,
                                                               'estimation_{}_{}_{}.pdf'.format(i, n, methods[m])))
            if m <= 8:
                errors[i, m, n] = simulator.mean_square_error(graphon, estimation)
            else:
                errors[i, m, n] = simulator.gw_distance(graphon, estimation)
            print('Data {}\tTrial {}\tMethod={}\tError={:.3f}\tTime={:.3f}sec'.format(
                i, n, methods[m], errors[i, m, n], time.time() - since))

print(np.mean(errors, axis=2))
with open(os.path.join(args.f_result, 'results_synthetic.pkl'), 'wb') as f:
    pickle.dump(errors, f)
