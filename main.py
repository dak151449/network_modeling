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



srvs, handlers, generato_data = download_config.get_services()

print(srvs, generato_data, handlers)



# const.tasks = [Task("test1", 1), Task("test2", 1), Task("test8", 1), Task("test9", 2), Task("test10", 2), Task("test3", 3), Task("test4", 3), Task("test5", 3), Task("test6", 3), Task("test7", 3), Task("test11", 1)]
# const.tasks = const.set_start_tasks(const.tasks)

const.tasks = []

g = Generator(handlers, generato_data)
print("Generator")

m = Model(Func_balancer("RoundRobinBalancer", srvs), srvs, g, get_types_hendlers(handlers))
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
    
