import download_config
from app.objects.task import Task
from app.objects.model import Model
from app.objects.balancer_functions.test import *
from app.global_constants import const
from app.stats.stats import *
from app.generate_task import Generator

def get_types_hendlers(hs):
    event_types = []
    for h in hs:
        event_types.append(h.id)
    return event_types



srvs, handlers, generato_data, b_max_length_queue_task, f_balancer  = download_config.get_services()

const.tasks = []

g = Generator(handlers, generato_data)
print("Generator")

m = Model(Func_balancer(f_balancer, srvs), srvs, g, get_types_hendlers(handlers), b_max_length_queue_task)
m.modeling()
print("END MODELING")
# print("CLOSE TASK")
# for s in const.closed_tasks:
#     print(s)
#     print("---------------------------")
# print()
# print("CLOSE SUBTASK")
# for s in const.subtask_closed:
#     print(s)
#     print("---------------------------")

print_stats(m, get_types_hendlers(handlers))

print_global_stat(m, get_types_hendlers(handlers))  
    
