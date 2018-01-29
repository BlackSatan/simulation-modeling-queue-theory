import generators
import math
import matplotlib.pyplot as plt
import one_channel_limit
import one_channel_unlimmited

# number of incoming requirements
N = 350
# intensity of incoming requirements
lambd = 12
# intensity of executing stream
mu = 23
# limit of queue, if 0 then queue has no limit
# m = 0
m = 3

incoming_dist = generators.exp_dist(N, lambd)
executing_dist = generators.exp_dist(N, mu)

ro = lambd / mu

idle_plot = []
executing_plot = []
queue_plot = []
reject_plot = []

print('Incoming requests intervals', incoming_dist)
print('Requests executing intervals', executing_dist)
print()

if m == 0:
    queue_plot = one_channel_limit.queue_plot(incoming_dist, executing_dist, 99)
    executing_plot = one_channel_limit.executing_plot(incoming_dist, executing_dist, 99)
    idle_plot = one_channel_limit.idle_plot(incoming_dist, executing_dist, 99)
    i_plot_x, i_plot_y = idle_plot
    print()
    print('==Theoretical state probabilities==')
    print()
    print(['p[' + str(i) + '] = ' + str(one_channel_unlimmited.state_probability(i, ro)) for i in range(0, 4)])
    print()
    print('==Queue properties==')
    print()
    print('System processing time =', sum(incoming_dist))
    print('System idle time =', str(sum(incoming_dist) * one_channel_unlimmited.state_probability(0, ro)))
    print('Total requests count =', len(incoming_dist))
    print('Rejected requests count =', math.floor(len(incoming_dist) * one_channel_unlimmited.rejection_probability()))
    print()
    print('Probability of request rejection, Preject =', one_channel_unlimmited.rejection_probability())
    print('Relative throughput, q =', one_channel_unlimmited.relative_throughput())
    print('Absolute throughput, A =', one_channel_unlimmited.absolute_throughput(lambd))
    print('Average count of queue items, k =', one_channel_unlimmited.average_queue_items_count(ro))
    print('Average count of executing items, w =', one_channel_unlimmited.average_system_items_count(ro))
    print('Average wait time of one request, Twait =', one_channel_unlimmited.average_queue_item_wait_time(ro, lambd))
    print('Average execute time of one request, Texecute =', one_channel_unlimmited.average_queue_item_execute_time(mu))
    print('Average service time of one request, Tservice =',
          one_channel_unlimmited.average_queue_item_total_time(ro, lambd, mu))
    print('Average idle time , Tidle =', one_channel_unlimmited.average_idle_time(ro, lambd))
else:
    queue_plot = one_channel_limit.queue_plot(incoming_dist, executing_dist, m)
    executing_plot = one_channel_limit.executing_plot(incoming_dist, executing_dist, m)
    idle_plot = one_channel_limit.idle_plot(incoming_dist, executing_dist, m)
    reject_plot = one_channel_limit.reject_plot(incoming_dist, executing_dist, m)
    i_plot_x, i_plot_y = idle_plot
    print('==Queue properties==')
    print()
    print('System processing time =', sum(incoming_dist))
    print('System idle time =', max(i_plot_y))
    print('Total requests count =', len(incoming_dist))
    print('Rejected requests count =', math.floor(len(incoming_dist) * one_channel_limit.rejection_probability(ro, m)))
    print()
    print('Probability of request rejection, Preject =', one_channel_limit.rejection_probability(ro, m))
    print('Relative throughput, q =', one_channel_limit.relative_throughput(ro, m))
    print('Absolute throughput, A =', one_channel_limit.absolute_throughput(ro, m, lambd))
    print('Average count of queue items, k =', one_channel_limit.average_queue_items_count(ro, m))
    print('Average count of executing items, w =', one_channel_limit.average_system_items_count(ro, m))
    print('Average wait time of one request, Twait =', one_channel_limit.average_queue_item_wait_time(ro, m, lambd))
    print('Average execute time of one request, Texecute =', one_channel_limit.average_queue_item_execute_time(mu))
    print('Average service time of one request, Tservice =', one_channel_limit.average_queue_item_total_time(ro, m, lambd, mu))
    print('Average idle time , Tidle =', one_channel_limit.average_idle_time(ro, m, lambd))


e_plot_x, e_plot_y = executing_plot
q_plot_x, q_plot_y = queue_plot
i_plot_x, i_plot_y = idle_plot
plt.plot(e_plot_x, e_plot_y, label='Items executing')
plt.plot(q_plot_x, q_plot_y, label='Queued items')
if m != 0:
    r_plot_x, r_plot_y = reject_plot
    plt.plot(r_plot_x, r_plot_y, label='Rejects requests count')
plt.legend()
plt.xlabel('t')
plt.show()

plt.plot(i_plot_x, i_plot_y, label='System idle')
plt.legend()
plt.xlabel('t')
plt.ylabel('idle time')
plt.show()

