import numpy as np


def get_random_color():
    return list(np.random.choice(range(256), size=3))