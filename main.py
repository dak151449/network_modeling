import download_config
from app.objects.task import Task
from app.objects.model import Model
from app.objects.balancer_functions.test import *
from app.global_constants import const
from app.stats.stats import *






srvs = download_config.get_services()

print(srvs)



const.tasks = [Task("test1", 1), Task("test2", 1), Task("test8", 1), Task("test9", 2), Task("test10", 2), Task("test3", 3), Task("test4", 3), Task("test5", 3), Task("test6", 3), Task("test7", 3), Task("test11", 1)]
const.tasks = const.set_start_tasks(const.tasks)

m = Model(test, srvs)
m.modeling()
print("END MODELING")
print("CLOSE TASK")
for s in const.closed_tasks:
    print(s)
    print("---------------------------")
print()
print("CLOSE SUBTASK")
for s in const.subtask_closed:
    print(s)
    print("---------------------------")

print_stats(m)
    
    
