from cdlib import NodeClustering, FuzzyNodeClustering, EdgeClustering
import json

__all__ = ["write_community_csv", "read_community_csv", "write_community_json",
           "read_community_json", "read_community_from_json_string"]


def write_community_csv(communities,  path, delimiter=","):
    """
    Save community structure to comma separated value (csv) file.

    :param communities: a NodeClustering object
    :param path: output filename
    :param delimiter: column delimiter

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_csv(coms, "communities.csv", ",")

    """
    with open(path, "w") as f:
        for cid, community in enumerate(communities.communities):
            res = delimiter.join(list(map(str, community)))
            f.write("%s\n" % res)


def read_community_csv(path, delimiter=",", nodetype=str):
    """
    Read community list from comma separated value (csv) file.

    :param path: input filename
    :param delimiter: column delimiter
    :param nodetype: specify the type of node labels, default str
    :return: NodeClustering object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_csv(coms, "communities.csv", ",")
    >>> coms = readwrite.read_community_csv(coms, "communities.csv", ",", str)

    """
    communities = []
    with open(path) as f:
        for row in f:
            community = list(map(nodetype, row.rstrip().split(delimiter)))
            communities.append(tuple(community))

    return NodeClustering(communities, None, "")


def write_community_json(communities, path):
    """
    Generate a JSON representation of the clustering object

    :param communities: a cdlib clustering object
    :param path: output filename
    :return: a JSON formatted string representing the object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_json(coms, "communities.json")
    """

    partition = {"communities": communities.communities, "algorithm": communities.method_name,
                 "params": communities.method_parameters, "overlap": communities.overlap, "coverage": communities.node_coverage}

    try:
        partition['allocation_matrix'] = communities.allocation_matrix
    except AttributeError:
        pass

    js_dmp = json.dumps(partition)
    with open(path, "w") as f:
        f.write(js_dmp)


def read_community_json(path):
    """
    Read community list from JSON file.

    :param path: input filename
    :return: a Clustering object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_json(coms, "communities.json")
    >>> readwrite.read_community_json(coms, "communities.json")
    """

    with open(path, "r") as f:
        coms = json.load(f)

    nc = NodeClustering([tuple(c) for c in coms['communities']], None, coms['algorithm'],
                        coms['params'], coms['overlap'])
    nc.node_coverage = coms['coverage']

    if 'allocation_matrix' in coms:
        nc.__class__ = FuzzyNodeClustering
        nc.allocation_matrix = coms['allocation_matrix']

    if type(nc.communities[0][0]) is list:
        cms = []
        for c in nc.communities:
            cm = []
            for e in c:
                cm.append(tuple(e))
            cms.append(tuple(cm))
        nc.communities = cms
        nc.__class__ = EdgeClustering

    return nc


def read_community_from_json_string(json_repr):
    """
    Read community list from JSON file.

    :param json_repr: json community representation
    :return: a Clustering object

    :Example:

    >>> import networkx as nx
    >>> from cdlib import algorithms, readwrite
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> readwrite.write_community_json(coms, "communities.json")
    >>> with open("community.json") as f:
    >>>     cr = f.read()
    >>>     readwrite.write_community_from_json_string(cr)
    """

    coms = json.loads(json_repr)

    nc = NodeClustering([tuple(c) for c in coms['communities']], None, coms['algorithm'],
                        coms['params'], coms['overlap'])
    nc.node_coverage = coms['coverage']

    if 'allocation_matrix' in coms:
        nc.__class__ = FuzzyNodeClustering
        nc.allocation_matrix = coms['allocation_matrix']

    if type(nc.communities[0][0]) is list:
        cms = []
        for c in nc.communities:
            cm = []
            for e in c:
                cm.append(tuple(e))
            cms.append(tuple(cm))
        nc.communities = cms
        nc.__class__ = EdgeClustering

    return nc
