import copy
import uuid

from . import task
from app.global_constants import const
from app.objects.pod import Pod
from app.objects.handler import Handler


# По сути это деплой те развернутый сервис в конкретном поде
class Service:
# ----------------------------------------------- 
    def __init__(self, name: str, hs: dict[int,Handler], count_pods: int, pods_w: list[int]) -> None:
        self.name: str = name
        """название сервиса (задается клиентом в конфиге)"""

        self.pods: list[Pod] = []
        
        self.hendlers: dict[int, Handler] = hs
        """словарь хендлеров у деплоя: id_хендлера -> handler"""
        
        for i in range(count_pods):
            if pods_w != None:
                self.pods.append(Pod(name, hs, pods_w[i]))
            else:
                self.pods.append(Pod(name, hs))
        
        
        
    def __str__(self):
        return f"name: {self.name}, \n handlers: {self.hendlers}"
    
    def set_task(self, pod_id: str, task: task.Task):
        """Задает новую задачу для poda у сервиса

        Args:
            task (task.Task): Новая задача
        """
        pass
    
    def update_time(self):
        """Обновляет состояние всех подов сервиса за 1 времени
        """
        for p in self.pods:
            if (not p.is_blocked) and len(p.queue_tasks) > 0:
                p.set_task()
            p.update_time()
    
    
    def update_metrics(self):
        """Обновляем метрики для анализа
        """
        
        for p in self.pods:
            p.update_metrics()
        
        return