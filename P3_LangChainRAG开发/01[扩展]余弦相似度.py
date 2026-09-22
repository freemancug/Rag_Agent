import numpy as np


def get_dot(vec_a, vec_b):
    """
    Calculate the dot product of two vectors.

    Args:
        vec_a (list): First vector.
        vec_b (list): Second vector.

    Returns:
        float: Dot product of the two vectors.
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be of the same length.")
    
    dot_sum=0
    for a, b in zip(vec_a, vec_b):
        dot_sum += a * b    
    return dot_sum

def get_norm(vec):
    """
    Calculate the Euclidean norm (magnitude) of a vector.

    Args:
        vec (list): Input vector.

    Returns:
        float: Euclidean norm of the vector.
    """
    sum_squares = 0
    for v in vec:
        sum_squares += v ** 2
    return np.sqrt(sum_squares)

def consine_similarity(vec_a, vec_b):
    """
    Calculate the cosine similarity between two vectors.

    Args:
        vec_a (list): First vector.
        vec_b (list): Second vector.

    Returns:
        float: Cosine similarity between the two vectors.
    """
    dot_product = get_dot(vec_a, vec_b)
    norm_a = get_norm(vec_a)
    norm_b = get_norm(vec_b)

    if norm_a == 0 or norm_b == 0:
        raise ValueError("One of the vectors is zero, cannot compute cosine similarity.")
    
    return dot_product / (norm_a * norm_b)

if __name__ == "__main__":
    vec_a = [0.5,0.5]
    vec_b = [0.7, 0.7]
    vec_c = [0.7,0.5]
    vec_d = [-0.6, -0.5]


    print("Cosine Similarity:ab:", consine_similarity(vec_a, vec_b))
    print("Cosine Similarity:ac:", consine_similarity(vec_a, vec_c))
    print("Cosine Similarity:ad:", consine_similarity(vec_a, vec_d))    