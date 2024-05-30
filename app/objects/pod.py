from collections import deque
import uuid
import copy
from typing import *

from app.objects.handler import Handler
# from app.objects.service import Service
from app.objects.task import Task
from app.global_constants import const

class Pod:

    def __init__(self, name: str, hs: dict[int, Handler], max_length_queue_task: int = 100 ,w: int = 1) -> None:
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
        self.is_cancel_actual_task: bool = False
        self.count_task_canceld: int = 0
 
        self.count_task_int_deque: list[int] = []
        """Количество задач в очереди с течением времени"""
        self.responces: list[Task] = []
        self.responces_time_avg: float = 0
        self.res_count: int = 0
        """список завершенных задач для статистики"""
        self.responces_count: list[int] = [0]
        """количество завершенных задач для статистики"""
        self.rps: list[float] = []
        # self.rp_count: int = 0
        """количество ответов за 1 времени"""
        
        self.busy_time: int = 1
        """Busy Time: Общее время, в течение которого устройство было занято обслуживанием транзакций."""
        self.idle_time: int = 0
        """Idle Time: Общее время, в течение которого устройство простаивало, то есть не выполняло никаких задач."""

        self.waiting_time_in_srv_queue = 0
        """общее время ожидания в очереди образа сервиса"""
        
        self.weight = w
        self.max_length_queue_task = max_length_queue_task
        
    def add_task(self, task: Task):
        """Добавляет задачи в очередь на обработку у пода

        Args:
            task (task.Task): Новая задача
        """
        
        if len(self.queue_tasks) >= self.max_length_queue_task:
            task.is_canceld = True
            self.count_task_canceld += 1
            return
        
        task.end_time_in_balancer_que = const.global_time
        task.start_time_in_pod_que = const.global_time
        self.queue_tasks.append(task)
        
        
        
    def update_time(self):
        """Обновляет состояние сервиса(деплоя)-пода за 1 времени
        """
        if self.actual_hendlers == None:
            return
        
        if self.is_cancel_actual_task == True and self.task_in_work != None:
            self.is_blocked = False
            self.task_in_work.is_canceld = True
            # self.task_in_work.end_work_time = const.global_time
            # self.task_in_work.end_global_time = const.global_time
            self.count_task_canceld += 1
            self.task_in_work = None
            self.is_cancel_actual_task = False
            self.wait_outer_hendler = False 
            return
        
        # print("Service.update_time", self.actual_hendlers, "-------- Serv:", self.name+self.id)
        if self.actual_hendlers.way != [] and not self.wait_outer_hendler:
            handler_id = self.actual_hendlers.way.pop()
            # создаем sub task и кладем её в балансировщик
            sub_task = None
            sub_task = Task(self.name+"_pod:"+self.id+str(uuid.uuid1()), handler_id, const.global_time)
            sub_task.stack_service = self.id
            # sub_task.start_global_time = const.global_time
            # sub_task.start_time_in_balancer_que = const.global_time
            const.tasks.append(sub_task)
            
            # заблокированы до ответа другой ручки
            self.wait_outer_hendler = True
            # print("Subtask  ", sub_task)
            return
        
        
        if not self.wait_outer_hendler and self.task_in_work != None:
            self.working_time -= 1
            
            if self.working_time <= 0:
                self.is_blocked = False
                self.task_in_work.end_work_time = const.global_time
                self.task_in_work.end_global_time = const.global_time
                self.task_in_work.is_closed = True
                
                # self.responces.append(self.task_in_work)
                self.res_count += 1
                 
                # self.busy_time += self.task_in_work.end_work_time - self.task_in_work.start_work_time
                
                self.responces_time_avg = self.busy_time / self.res_count
                
                self.task_in_work = None
                # const.update_task_is_closed(self.task_in_work.id)
        return
            
    def update_metrics(self):
        """Обновляем метрики для анализа
        """
        self.count_task_int_deque.append(len(self.queue_tasks))
        
        
        # глоабльное время работы устройства
        if self.is_blocked:
            self.busy_time += 1
        else:
            self.idle_time += 1
            
        self.rps.append(self.res_count / (self.busy_time))
        
        # self.responces_count.append(self.res_count)
        return
    
    def set_task(self):
        """Задает новую задачу для сервиса в поде

        Args:
            task (task.Task): Новая задача
        """
        
        self.task_in_work = self.queue_tasks.popleft()
        # print("Pod.update_time:", self.actual_hendlers)
        self.actual_hendlers = copy.deepcopy(self.hendlers.get(self.task_in_work.handler_id))
        self.is_blocked = True
        self.working_time = self.actual_hendlers.local_time
        
        self.task_in_work.end_time_in_pod_que = const.global_time
        self.task_in_work.start_work_time = const.global_time
        
        self.waiting_time_in_srv_queue += const.global_time - self.task_in_work.start_time_in_pod_que
        return
    
    def cancel_actual_task(self):
        self.task_in_work.is_canceld = True
        self.count_task_canceld += 1