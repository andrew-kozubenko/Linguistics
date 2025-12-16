def extract_label(params_values: dict):
    labels = params_values.get(
        "http://www.w3.org/2000/01/rdf-schema#label", []
    )
    for l in labels:
        if l.endswith("@ru"):
            return l.replace("@ru", "")
    return labels[0].replace("@en", "") if labels else None


def extract_comment(params_values: dict):
    return params_values.get(
        "http://www.w3.org/2000/01/rdf-schema#comment"
    )
