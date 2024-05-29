# from app.objects.balancer import Balancer
from app.objects.task import Task



STOP_TIME = 10000 * 50
"""остановка моделирования по истечению времени
"""

global_time = 1
# b = Balancer(test)
tasks: list[Task] = []
closed_tasks: list[Task] = []
subtask_closed: list[Task] = []

# def update_task_is_closed(task_id: str):
#     for i in range(len(tasks)):
#         if tasks[i].id == task_id:
#             tasks[i].is_closed = True
#             tasks[i].end_global_time = global_time
#             return
        
    
        
def set_start_tasks(tasks: list[Task]) -> list[Task]:
    for t in tasks:
        t.start_global_time = global_time
    return tasks

def get_time():
    return global_time

def sleep(duration):
    return global_time