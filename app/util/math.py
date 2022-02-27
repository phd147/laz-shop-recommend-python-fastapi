from scipy import spatial


def calculate_cosine_similarity(a, b):
    cosine_distance = 1 - float(spatial.distance.cosine(a, b))
    return cosine_distance
