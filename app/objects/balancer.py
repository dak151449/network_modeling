import copy

from . import pod
from app.global_constants import const
from app.objects.service import Service

class Balancer:
    # tasks: list[task.Task] = []
    """список задач на входе"""
    srvs: dict[str, Service] = {}
    """по названию сервиса возвращает список подов для него
    """
    handler_id_to_service_name: dict[int, str]  = {}
    """сопоставление по хендлеру имя сервиса"""
    
    balance_f = None
    """функция балансировки
    """
    
    # closed_tasks: list[task.Task] = []
    tx_stats_balance_time: dict[any, int] = {}
    tx_stats_time: dict[any, int] = {}
    """словарь тип транзакции -> общее време прибывания в системе всех таких транзакций""" 
    tx_stats_count: dict[any, int] = {}
    """словарь тип транзакции -> общее количество таких транзакций"""
    tx_stats_count_canceld: dict[any, int] = {}
    """словарь тип транзакции -> общее количество отмененных таких транзакций"""
    
    
    def __init__(self, f_b, srvs: list[Service], types_tx) -> None:
        self.balance_f = f_b.balance_f
        # сгенерировать 3 пода и сервисы им
        
        for tx in types_tx:
            self.tx_stats_count[tx] = 0
            self.tx_stats_time[tx] = 0
            self.tx_stats_count_canceld[tx] = 0
            self.tx_stats_balance_time[tx] = 0
            
        for s in srvs:
            self.srvs[s.name] = s
            
            for k in list(s.hendlers.keys()):
                self.handler_id_to_service_name[k] = s.name
        
        print(self.srvs)
        print(self.handler_id_to_service_name)
        
        return
    
    def get_func_balance(self):
        balance_count = 10
        
        # print("get_func_balance", const.tasks)
        # for i in range(min(balance_count, len(const.tasks))):
        i = 0
        count_new_task = 0
        while count_new_task < min(balance_count, len(const.tasks)) and i < len(const.tasks):
            # if const.tasks[i].stack_service != -1:
            # print("Task " + const.tasks[i].id, const.tasks[i].is_closed, const.tasks[i].in_work)
            if not const.tasks[i].is_closed and not const.tasks[i].in_work:
                handler_id = const.tasks[i].handler_id
                
                ## по handler_id доставать имя сервиса
                service_name = self.get_service_name_by_hendler_id(handler_id)
                # print("get_service_name_by_hendler_id-", service_name, handler_id)
                actual_pods, act_pods_ids = self.get_pods_by_srv_id(service_name)
                if actual_pods == []:
                    i += 1
                    continue
                t, new_pods = self.balance_f(const.tasks[i], actual_pods)
       
                self.update_pods(service_name, new_pods, act_pods_ids)
                const.tasks[i].in_work = True
                count_new_task += 1
                
                self.tx_stats_balance_time[const.tasks[i].handler_id] = (self.tx_stats_balance_time[const.tasks[i].handler_id] + const.global_time - const.tasks[i].start_time_in_balancer_que) / 2
            elif const.tasks[i].is_closed:
                t = const.tasks[i]
                del const.tasks[i]

                if t.stack_service != -1:
                    # update pod->service-> .wait_outer_hendler = False
                    # надо найти конкретный под и сервис

                    check = False
                    for pi in self.srvs:
                        for p in self.srvs[pi].pods:
                            if p.id == t.stack_service:
                                p.wait_outer_hendler = False
                                check = True
                                break
                        if check:
                            break
                        
                    # const.subtask_closed.append(t)
                # const.closed_tasks.append(t)
                self.tx_stats_count[t.handler_id] += 1
                self.tx_stats_time[t.handler_id] += t.end_global_time - t.start_global_time
            elif const.tasks[i].is_canceld:
                t = const.tasks[i]
                del const.tasks[i]
                if t.stack_service != -1:
                    check = False
                    for pi in self.srvs:
                        for p in self.srvs[pi].pods:
                            if p.id == t.stack_service:
                                p.is_cancel_actual_task = True
                                check = True
                                break
                        if check:
                            break
                self.tx_stats_count_canceld[t.handler_id] += 1
                
            i += 1      
        return
    
    def get_pods_by_srv_id(self, srv_id: str) -> pod.Union[list[pod.Pod], list[int]]:
        """по названию сервиса находит список подов с нужной ручкой
            и список их индексов в общем массиве

        Args:
            srv_id (int): id хендлера

        Returns:
            pod.Union[list[pod.Pod], list[int]]: список подов содержащих сервис с нужной ручкой
            и список их индексов в общем массиве
        """
        
        srv = self.srvs.get(srv_id)
        
        actual_pod = []
        actual_pod_ids = []
        for i in range(len(srv.pods)):
            if srv.pods[i].is_blocked and False:
                continue
            actual_pod.append(srv.pods[i])
            actual_pod_ids.append(i)
        
        return actual_pod, actual_pod_ids 
    
    def update_pods(self, service_id: str, new_pods: list[pod.Pod], ids: list[int]):
        """вставляет измененные поды в замен старых по индексам ids

        Args:
            service_id (int): название сервиса
            new_pods (list[pod.Pod]): список обновленных подов для сервиса с service_id
            ids (list[int]): индексы куда надо вставлять новые поды в списке pods
        """
        for i in range(len(ids)):
            self.srvs[service_id].pods[ids[i]] = new_pods[i]
            
    def update_time(self):
        """обновление во всей системе
        """
        
        for k in self.srvs:
            # print("Update time:", k, "++++++++++++++++++++++++++")
            self.srvs[k].update_time()
        return
    
    def get_service_name_by_hendler_id(self, handler_id: int) -> str:
        """по handler_id возвращает имя сервиса

        Args:
            handler_id (int): номер хендлера

        Returns:
            str: названеи сервиса, который содержит данный хендлер
        """
        return self.handler_id_to_service_name.get(handler_id)


    def update_metrics(self):
        for k in self.srvs:
            self.srvs[k].update_metrics()
        return