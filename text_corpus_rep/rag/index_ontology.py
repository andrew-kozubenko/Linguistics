from rag.node_to_text import node_to_text
from rag.embeddings import embed


def build_ontology_index(nodes, edges):
    nodes_by_uri = {
        n["id"]: n for n in nodes
        if "id" in n
    }

    texts = []
    meta = []

    for node in nodes:
        text = node_to_text(node, edges, nodes_by_uri)
        if not text.strip():
            continue

        texts.append(text)
        meta.append({
            "node_id": node["id"],
            "text": text
        })

    vectors = embed(texts)

    return {
        "vectors": vectors,
        "meta": meta
    }
