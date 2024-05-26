
from app.objects.balancer import Balancer
from app.objects.service import Service
from app.global_constants import const


class Model:
    balancer: Balancer = None
    
    def __init__(self, f, srvs: list[Service]):
        self.balancer = Balancer(f, srvs)
        
    def modeling(self):
        
        while const.global_time < const.STOP_TIME:
            self.run_step()
            print("------------------------- global time =", const.global_time, "TASK:", const.tasks)
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
        
        return