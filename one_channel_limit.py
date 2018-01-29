def idle_probability(ro, m):
    return 1.0 / (
        1 + (ro ** 2 / (1 - ro)) * (1 - ro ** m)
    )

def rejection_probability(ro, m):
    return ro ** (m + 1) * idle_probability(ro, m)


def relative_throughput(ro, m):
    return average_queue_items_count(ro, m) / average_system_items_count(ro, m)


def absolute_throughput(ro, m, lambd):
    return lambd * relative_throughput(ro, m)


def average_queue_items_count(ro, m):
    return ro ** 2 * (1 - ro ** m) * (m + 1 - m * ro) / ((1 - ro ** (m + 2)) * (1 - ro))


def average_system_items_count(ro, m):
    return (ro + ro ** (m + 2)) / (1 - ro ** (m + 2))


def average_items_count(ro, m):
    return average_queue_items_count(ro, m) + average_system_items_count(ro, m)


def average_queue_item_wait_time(ro, m, lambd):
    return average_queue_items_count(ro, m) / lambd


def average_queue_item_execute_time(mu):
    return 1 / mu


def average_queue_item_total_time(ro, m, lambd, mu):
    return average_queue_item_wait_time(ro, m, lambd) + relative_throughput(ro, m) / mu


def average_idle_time(ro, m, lambd):
    return average_queue_item_wait_time(ro, m, lambd) / absolute_throughput(ro, m, lambd)


def find_exec_time(arrival_time, exec_arr):
    last_exec = exec_arr[-1]
    return max(arrival_time, last_exec[1])


def system_run(incoming_dist, executing_dist, m):
    result = []
    time = 0
    for index, inc in enumerate(incoming_dist):
        exc = executing_dist[index]
        if index == 0:
            time += inc + exc
            result.append([inc, inc + exc])
        else:
            arrival_time = sum(incoming_dist[:index])
            start = find_exec_time(arrival_time, result)
            queued_items_count = sum(list(map(lambda st: 1 if st[0] > arrival_time else 0, result)))
            if queued_items_count > m:
                continue
            result.append([start, start + exc])
    return result


def executing_plot(incoming_dist, executing_dist, m):
    result = system_run(incoming_dist, executing_dist, m)
    x = []
    y = []
    for index, coord in enumerate(result):
        x.append(coord[1])
        y.append(index)
    return x, y


def queue_plot(incoming_dist, executing_dist, m):
    result = system_run(incoming_dist, executing_dist, m)
    x = []
    y = []
    arrival_times = [
        sum(incoming_dist[:index])
        for index, i in enumerate(incoming_dist)
    ]
    for index, coord in enumerate(result):
        arrival_time = arrival_times[index]
        if arrival_time < coord[0]:
            y.append(len(list(filter(lambda arr_time: arr_time < coord[0], arrival_times[index:]))))
            x.append(coord[0])
        else:
            y.append(0)
            x.append(coord[0])
    return x, y


def idle_plot(incoming_dist, executing_dist, m):
    result = system_run(incoming_dist, executing_dist, m)
    x = []
    y = []
    idle = 0
    last_time = None
    for index, coord in enumerate(result):
        if last_time is None:
            idle = coord[0]
        else:
            idle += max(0, coord[0] - last_time)
        last_time = coord[1]
        y.append(idle)
        x.append(last_time)
    return x, y


def reject_plot(incoming_dist, executing_dist, m):
    result = system_run(incoming_dist, executing_dist, m)
    x = []
    y = []
    arrival_times = [
        sum(incoming_dist[:index])
        for index, i in enumerate(incoming_dist)
    ]
    rejects = 0
    for index, arrival_time in enumerate(arrival_times):
        qcount = 0
        for iindex, coord in enumerate(result):
            qcount = qcount if arrival_times[iindex] > arrival_time or coord[1] < arrival_time else qcount + 1
        if qcount > m:
            rejects += 1
        y.append(rejects)
        x.append(arrival_time)
    return x, y