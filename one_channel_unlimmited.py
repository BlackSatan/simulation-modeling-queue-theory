def state_probability(k, ro):
    return ro ** k * (1 - ro)


def rejection_probability():
    return 0


def relative_throughput():
    return 1


def absolute_throughput(lambd):
    return lambd


def average_queue_items_count(ro):
    return ro ** 2 / (1 - ro)


def average_system_items_count(ro):
    return ro


def average_items_count(ro):
    return average_queue_items_count(ro) + average_system_items_count(ro)


def average_queue_item_wait_time(ro, lambd):
    return average_queue_items_count(ro) / lambd


def average_queue_item_execute_time(mu):
    return 1 / mu


def average_queue_item_total_time(ro, lambd, mu):
    return average_queue_item_wait_time(ro, lambd) + average_queue_item_execute_time(mu)


def average_idle_time(ro, lambd):
    return average_queue_item_wait_time(ro, lambd) / absolute_throughput(lambd)
