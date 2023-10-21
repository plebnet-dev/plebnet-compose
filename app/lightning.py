
from collections import namedtuple
import json
import networkx as nx
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_describegraph_json(filename):
    """load edge information from an lnd network dump"""
    # set up namedtuples so we can access the sample data in the same manner as grpc response data
    Response = namedtuple('Response', ['nodes', 'edges'] )
    Node = namedtuple('Node', ['last_update', 'pub_key', 'alias', 'addresses', 'color', 'features'])
    Edge = namedtuple('Edge', ['channel_id', 'chan_point', 'last_update', 'node1_pub', 'node2_pub', 'capacity', 'node1_policy', 'node2_policy'])
    RoutingPolicy = namedtuple('RoutingPolicy', ['time_lock_delta', 'min_htlc', 'fee_base_msat', 'fee_rate_milli_msat', 'max_htlc_msat', 'last_update', 'disabled'])

    with open(filename) as f:
        dg = json.load(f)

    nodes = [Node(**node) for node in dg['nodes']]
    edges = []
    for edge in dg['edges']:
        for policy in 'node1_policy', 'node2_policy':
            if edge[policy] is not None:
                try:
                    edge[policy] = RoutingPolicy(**edge[policy])
                except:
                    logging.error(edge[policy])
                    raise
        edges.append(Edge(**edge))
    return Response(nodes, edges)

def get_features(features):
    results = {}
    for k, f in features.items():
        try:
            results[k] = dict(name=f.name,
                     is_required=f.is_required,
                     is_known=f.is_known,)
        except:
            logging.error(f)
            raise
    return results


def get_node_multigraph(response):
    MG = nx.MultiDiGraph()

    MG.add_nodes_from(((node.pub_key,
                        dict(alias=node.alias,
                             pub_key=node.pub_key,
                             color=node.color,
#                              features=get_features(node.features),
                             last_update=node.last_update)) for node in response.nodes))
    # MG.number_of_nodes()

#     Add edges. Use `channel_id` as edge keys to so future updates don't duplicate edges.

    edge_iterable = [(edge.node1_pub,
                      edge.node2_pub,
                      edge.channel_id,
                      dict(capacity=edge.capacity,
                           node1_policy=edge.node1_policy,
                           node2_policy=edge.node2_policy)) for edge in response.edges]

    channel_ids = MG.add_edges_from(edge_iterable)
    MG.number_of_edges()
    return MG


def assign_capacity(G):
    """This is the sum of channel capacities available to a given node.
    This will be used to compute initial positions in the layout."""
    G.add_nodes_from(((k, dict(capacity=v)) for k,v in G.degree(weight='capacity')))
    return G 

def get_directed_nodes(MG):
    DG = nx.DiGraph()

    # Insert all node information from multi grid graph

    DG.add_nodes_from(MG.nodes(data=True))

    # Accumulate capacity for all duplicate edges.

    for node, neighbors in MG.adjacency():
    #     print(node, MG.nodes[node]['alias'])
        for neighbor, v in neighbors.items():
    #         print('\t{}:'.format(neighbor))
            capacity = 0
            avg_fee = 0
            avg_N = 1
            for k_, v_ in v.items():
                capacity += int(v_['capacity'])
                # running average
                if v_['node1_policy'] is not None:
                    avg_fee += (int(v_['node1_policy'].fee_rate_milli_msat) + avg_fee)/(avg_N+1)
                    avg_N += 1
                if v_['node2_policy'] is not None:
                    avg_fee += (int(v_['node2_policy'].fee_rate_milli_msat) + avg_fee)/(avg_N+1)
                    avg_N += 1
    #             print('\t\t{}: {}'.format(k_, v_))
            DG.add_edge(node,
                       neighbor,
                       capacity=capacity,
                       avg_fee=avg_fee,
                      )
    return DG


def load_graph_data(limit=100):
    response = get_describegraph_json('describegraph.json')

    MG = get_node_multigraph(response)
    DG = assign_capacity(get_directed_nodes(MG))
    G = DG.to_undirected()

    degrees = dict(G.degree())
    nodes = []

    for node in G.nodes():
        node_data = G.nodes[node]
        degree = degrees[node]
        nodes.append((node_data['alias'], degree, node_data['color']))

    # Sort by degree (in descending order) and take the top 100 nodes
    sorted_nodes = sorted(nodes, key=lambda x: x[1], reverse=True)[:limit]

    return sorted_nodes




