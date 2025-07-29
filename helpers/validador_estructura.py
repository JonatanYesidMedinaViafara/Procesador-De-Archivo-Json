def es_estructura_valida(data):
    if not isinstance(data, list):
        return False

    for documento in data:
        if not isinstance(documento, dict):
            return False
        if "data_extraida" not in documento:
            return False
        if not isinstance(documento["data_extraida"], dict):
            return False

    return True

