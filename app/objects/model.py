
from app.objects.balancer import Balancer
from app.objects.service import Service
from app.global_constants import const
from app.generate_task import Generator


class Model:
    balancer: Balancer = None
    
    def __init__(self, f, srvs: list[Service], g: Generator, types_tx, b_max_length_queue_task):
        self.balancer = Balancer(f, srvs, types_tx, b_max_length_queue_task)
        self.generator = g
        self.b_max_length_queue_task = b_max_length_queue_task
        self.balancer_count_canceled: dict[any, int] = {}
        for s in srvs:
            for h in s.hendlers:
                self.balancer_count_canceled[h] = 0
            
    def modeling(self):
        
        while const.global_time < const.STOP_TIME:
            self.run_step()
            if const.global_time % 10000 == 0:
                print("------------------------- global time =", const.global_time)
            const.global_time +=1
        
        return
    
    def run_step(self):
        """Шаг 1 времени в мире
        """
        # положить задачи от балансировщика к подам
        self.balancer.get_func_balance()
        
        # надо обновить все время у каждой задачи в работе если время 0 вернуть балансеру в очередь или если нужен вызов стороннего сервиса
        self.balancer.update_time()
        
        
        self.balancer.update_metrics()
        
        self.generator.schedule_events()
        
        self.check_cancel_task()
        
        return
    
    def check_cancel_task(self):
        if len(const.tasks) > self.b_max_length_queue_task:
            get_cancel_t = const.tasks[self.b_max_length_queue_task:]
            for t in get_cancel_t:
                t.is_canceled = True
                self.balancer_count_canceled[t.handler_id] += 1

        return