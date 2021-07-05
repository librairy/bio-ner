def group_in_dict(normalized_ent):
    normalized_ents = {}
    for k, v in [(key, d[key]) for d in normalized_ent for key in d]:
        if k not in normalized_ents:
            if isinstance(v, list):
                normalized_ents[k] = v
            else:
                normalized_ents[k] = [v]
        else:
            if v not in normalized_ents[k]:
                if isinstance(v, list):
                    normalized_ents[k] += v
                else:
                    normalized_ents[k].append(v)
    return normalized_ents
