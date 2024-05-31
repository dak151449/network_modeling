# from app.objects.balancer import Balancer
from app.objects.task import Task



STOP_TIME = 10000 * 50
"""остановка моделирования по истечению времени
"""

global_time = 1
tasks: list[Task] = []
closed_tasks: list[Task] = []
subtask_closed: list[Task] = []

    
        
def set_start_tasks(tasks: list[Task]) -> list[Task]:
    for t in tasks:
        t.start_global_time = global_time
    return tasks

def get_time():
    return global_time

def sleep(duration):
    return global_time