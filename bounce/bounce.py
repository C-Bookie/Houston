import random
from math import pi

import matplotlib.pyplot as plt
import numpy as np

bumps = 5
points = 100


def mountain_noise(points):
    y = [
        random.random() * 1
        # (min(n/points, (points-n)/points))
        for n in range(points)
    ]
    return y


def test1():
    x_max = bumps * (pi * 2) + pi
    x = np.arange(0, x_max, (x_max / points))

    y = np.cos(x)
    # y *= mountain_noise(points)
    y += 1
    y /= 2
    y *= np.linspace(bumps * pi, 0, 100)
    y = np.full(points, 1) - y

    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    test1()
