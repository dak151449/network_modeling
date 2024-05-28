import sched
import random
import numpy as np
import uuid

from app.objects.task import Task
from app.objects.handler import Handler
from app.global_constants import const

class Generator():
    
    def __init__(self, handlers: list[Handler], data: dict[str, int]):
        # Создаем планировщик
        self.scheduler = sched.scheduler(const.get_time, const.sleep)

        # Типы событий
        self.event_types = []
        # Вероятности для каждого типа события (должны суммироваться до 1)
        self.probabilities = []
        for h in handlers:
            self.event_types.append(h.id)
            self.probabilities.append(h.probability)
        
        # Время между событиями (в секундах)
        print(data)
        self.interval = data["interval"]
        self.count = data["count_in_iteration"]
        self.start_time = const.get_time()
        # # Планируем первое событие
        # self.schedule_events()

        # Запускаем планировщик
        # self.scheduler.run()
        return
    
    # def generate_uniform_values(self):
    #     return np.linspace(start, end, num_values).tolist()
    
    def generate_random_task(self) -> Task:
        if random.randint(0, 1):
            return Task(str(uuid.uuid1()), random.randint(1, 4))
        
        
    def schedule_events(self):

        if const.get_time() % self.interval != 0:
            return
        
        for _ in range(self.count):
            # Выбираем тип события по заданному распределению
            event_type = np.random.choice(self.event_types, p=self.probabilities)
            
            self.generate_event(event_type)
        
    def generate_event(self, event_type: int):
        const.tasks.append(Task(str(uuid.uuid1()), event_type))
        return 
        
    
