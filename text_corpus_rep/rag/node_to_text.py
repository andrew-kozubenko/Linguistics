from rag.rdf_utils import extract_label, extract_comment


def node_to_text(node, edges, nodes_by_uri):
    data = node.get("data", {})
    params = data.get("params_values", {})

    uri = data.get("uri")
    label = extract_label(params)
    comment = extract_comment(params)

    lines = []

    if label:
        lines.append(f"Название: {label}")

    if comment:
        lines.append(f"Описание: {comment}")

    # Типы (Class / NamedIndividual)
    types = [
        l.split("#")[-1]
        for l in data.get("labels", [])
        if "owl#" in l
    ]
    if types:
        lines.append(f"Тип: {', '.join(types)}")

    # Связи
    for e in edges:
        if e.get("from") == node["id"]:
            target_node = nodes_by_uri.get(e.get("to"))
            if not target_node:
                continue

            rel = e.get("label") or e.get("type")
            target_label = extract_label(
                target_node["data"].get("params_values", {})
            )

            if rel and target_label:
                lines.append(f"{rel}: {target_label}")

    return "\n".join(lines)
