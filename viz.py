import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import matplotlib.pyplot as plt

def draw_graph(relations):
    G = nx.MultiDiGraph(relations)
    A = to_agraph(G)
    A.layout()
    for x in G.nodes:
        A.get_node(x).attr['shape'] = 'circle'
        A.get_node(x).attr['label'] = ''
        A.get_node(x).attr['color'] = 'blue'
        A.get_node(x).attr['height'] = .4
        A.get_node(x).attr['width'] = .4
    A.draw('multi.png')
    #plt.show()
