from collections import deque
import uuid
import copy
from typing import *

from app.objects.handler import Handler
# from app.objects.service import Service
from app.objects.task import Task
from app.global_constants import const

class Pod:

    def __init__(self, name: str, hs: dict[int, Handler]) -> None:
        self.id  = str(uuid.uuid1())
        self.queue_tasks: deque = deque()
        
        self.name: str = name
        """Название сервиса (задается клиентом в конфиге)"""
        self.task_in_work: Task = None
        """актуальная задача"""
        self.working_time: int = 0
        """время обработки задачи, выставляет, когда задача беертся в работу и изменяется до нуля с течением времени"""
        self.is_blocked: bool = False
        """флаг, который показывает, что деплой занят """
        self.wait_outer_hendler: bool = False
        """флаг который блокирует выполнение задачи из-за запроса во внешний сервис"""
        self.hendlers: dict[int, Handler] = hs
        """словарь хендлеров у деплоя: id_хендлера -> handler"""
        self.actual_hendlers: Handler = None
        """активный Handler"""
 
        self.count_task_int_deque: list[int] = []
        """Количество задач в очереди с течением времени"""
        self.responces: list[Task] = []
        """список завершенных задач для статистики"""
        self.rps: list[float] = []
        # self.rp_count: int = 0
        """количество ответов за 1 времени"""
    
    def add_task(self, task: Task):
        """Добавляет задачи в очередь на обработку у пода

        Args:
            task (task.Task): Новая задача
        """
        self.queue_tasks.append(task)
        
        
        
    def update_time(self):
        """Обновляет состояние сервиса(деплоя)-пода за 1 времени
        """
        if self.actual_hendlers == None:
            return
        
        print("Service.update_time", self.actual_hendlers, "-------- Serv:", self.name+self.id)
        if self.actual_hendlers.way != [] and not self.wait_outer_hendler:
            handler_id = self.actual_hendlers.way.pop()
            # создаем sub task и кладем её в балансировщик
            sub_task = Task(self.name+"_pod:"+self.id+str(uuid.uuid1()), handler_id)
            sub_task.stack_service = self.id
            sub_task.start_global_time = const.global_time
            const.tasks.append(sub_task)
            
            # заблокированы до ответа другой ручки
            self.wait_outer_hendler = True
            print("Subtask  ", sub_task)
            return
        
        
        if not self.wait_outer_hendler:
            self.working_time -= 1
            
            if self.working_time <= 0:
                self.is_blocked = False
                self.responces.append(self.task_in_work)
                const.update_task_is_closed(self.task_in_work.id)
        return
            
    def update_metrics(self):
        """Обновляем метрики для анализа
        """
        self.count_task_int_deque.append(len(self.queue_tasks))
        self.rps.append(len(self.responces) / (const.global_time))
        return
    
    def set_task(self):
        """Задает новую задачу для сервиса в поде

        Args:
            task (task.Task): Новая задача
        """
        
        self.task_in_work = self.queue_tasks.popleft()
        print("Pod.update_time:", self.actual_hendlers)
        self.actual_hendlers = copy.deepcopy(self.hendlers.get(self.task_in_work.handler_id))
        self.is_blocked = True
        # print("----------", task.id, task.handler_id, self.actual_hendlers, self.hendlers)
        # print(self)
        self.working_time = self.actual_hendlers.local_time
        
        return