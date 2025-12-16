import json

def find_edges(obj):
    edges = []
    if isinstance(obj, dict):
        if obj.get("type") == "mainEdge":
            edges.append(obj)
        for v in obj.values():
            edges.extend(find_edges(v))
    elif isinstance(obj, list):
        for item in obj:
            edges.extend(find_edges(item))
    return edges

def load_ontology(path):
    with open(path, encoding="utf-8") as f:
        g = json.load(f)

    nodes = g.get("nodes", [])
    edges = find_edges(g)

    print(f"Узлов: {len(nodes)}, связей: {len(edges)}")
    return nodes, edges
