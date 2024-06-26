import random
import numpy as np
import uuid

from app.objects.task import Task
from app.objects.handler import Handler
from app.global_constants import const
from app.distributions.distributions import Distributions


class Generator():
    def __init__(self, handlers: list[Handler], data: dict[str, int]):
        # Типы событий
        self.event_types = []
        # Вероятности для каждого типа события (должны суммироваться до 1)
        self.probabilities = []
        for h in handlers:
            self.event_types.append(h.id)
            self.probabilities.append(h.probability)
        
        # Время между событиями (в секундах)
        self.interval_static = data["interval"]
        self.interval = data["interval"]
        self.count = data["count_in_iteration"]
        self.start_time = const.get_time()
        
        self.func_distr: str = data["distribution"][0]["function_name"]
        self.func_distr_args: list[any] = data["distribution"][0]["function_args"]
        return
    
    def generate_random_task(self) -> Task:
        if random.randint(0, 1):
            return Task(str(uuid.uuid1()), random.choice(self.event_types), const.global_time)
        
        
    def schedule_events(self):

        if const.get_time() % self.interval != 0:
            return
        
        for _ in range(self.count):
            # Выбираем тип события по заданному распределению
            event_type = np.random.choice(self.event_types, p=self.probabilities)
            
            self.generate_event(event_type)
        
        self.interval = self.interval_static + Distributions.uniform(*self.func_distr_args)
        
    def generate_event(self, event_type: int):
        const.tasks.append(Task(str(uuid.uuid1()), event_type, const.global_time))
        
        const.all_task_count += 1
        
        return 
        
    
