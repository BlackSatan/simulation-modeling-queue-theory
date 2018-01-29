import random


def exp_dist(n, lambd):
    return [random.expovariate(lambd) for i in range(0, n)]
