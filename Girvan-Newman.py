from itertools import count
import networkx as nx

data_path = './data/test1.txt'
# vertices must be split by a blank:' '

def build_graph(G, filename):
    '''
    read files from text file
    '''
    f = open(filename)
    dim = int(f.readline())
    for i in range(dim):
        line = f.readline().split(' ')
        for j in range(dim):
            if int(line[j]) != 0:
                G.add_edge(i, j, weight=int(line[j]))
def do_iteration(G):
    '''
    delete the edge(s) with the maxium betweenness
    '''
    init_comp = nx.number_connected_components(G)
    comp = init_comp
    while comp <= init_comp:
        betweenness = figure_betweenness(G)
#         print(betweenness)
        max_betweenness = max(betweenness.values())
        for k, v in betweenness.items():
                if v == max_betweenness:
                    G.remove_edge(k[0],k[1])
        comp = nx.number_connected_components(G)
    return nx.connected_components(G)





def modularity(G, ori_G):
    '''
    figure out the modularity of the graph
    '''
    weight = None
    communities = nx.connected_components(G)
    m = ori_G.size()
    degree = dict(ori_G.degree())
    norm = 1.0 / (2 * m)
    def val(u, v):
        try:
            w = 1
            tmp = ori_G[u][v]
        except KeyError:
            w = 0
        res = w - degree[u] * degree[v] * norm
#         print(res)
        return res
    Q = 0.0
    for c in communities:
        for u in c:
            for v in c:
                Q += val(u, v)
    return Q * norm


def figure_betweenness(G):
    '''
    figure out the betweenness of the every two nodes
    '''
    betweenness = dict.fromkeys(G, 0.0)
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    nodes = G

    for node in nodes:
        betweenness = bfs(G, node, betweenness)
    for n in G:
        del betweenness[n]
    return betweenness



def bfs(G, node, betweenness):
    '''
    bfs algorithm to figure shortest node to node v
    '''
    path = []
    path_dic = {}
    for v in G:
        path_dic[v] = []
    sigma = dict.fromkeys(G, 0)
    dis = {}
    sigma[node] = 1
    dis[node] = 0
    queue = [node]
    while queue:
        v = queue.pop(0)
        path.append(v)
        dis_v = dis[v]
        sig_v = sigma[v]
        for adj_v in G[v]:
            if adj_v not in dis:
                queue.append(adj_v)
                dis[adj_v] = dis_v + 1
            if dis[adj_v] == dis_v + 1:
                sigma[adj_v] += sig_v
                path_dic[adj_v].append(v)
#     print(path)
#     print(path_dic)
#     print(sigma)
    delta = dict.fromkeys(path, 0)
    while path:
        w = path.pop()
        coeff = (1 + delta[w]) / sigma[w]
        for v in path_dic[w]:
            c = sigma[v] * coeff
            if (v, w) not in betweenness:
                betweenness[(w, v)] += c
            else:
                betweenness[(v, w)] += c
            delta[v] += c
        if w != node:
            betweenness[w] += delta[w]
    return betweenness




if __name__ == '__main__':
    '''
    the loop until no edges in the graph is in this main function
    '''
    G = nx.Graph()
    ori_G = nx.Graph()
    build_graph(G, data_path)
    build_graph(ori_G, data_path)
    res_dic = {}
    comp_lst = []
    mod_lst = []
    while G.number_of_edges():
        tmp = list(do_iteration(G))
        mod = modularity(G, ori_G)
        comp_lst.append(tmp)
        mod_lst.append(mod)
        res_dic[mod] = tmp
    print('\nnetwork decomposition:')
    for comp in comp_lst:
        print(comp)
    print('\n')

    for index in range(len(mod_lst)):
        print('{0} clusters: modularity {1}'.format(len(comp_lst[index]), mod_lst[index]))
    print('optimal structure: {0}'.format(res_dic[sorted(res_dic.keys())[-1]]))