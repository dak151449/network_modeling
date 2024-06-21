import random

from app.objects.pod import Pod
from app.objects.service import Service

class Func_balancer:
    def __init__(self, name_f, srv_t: list[Service]):
        self.fs: dict[str, function] = {"test": self.test,
                                        "LeastResponseTimeBalancer": self.LeastResponseTimeBalancer,
                                        "LeastConnectionsBalancer": self.LeastConnectionsBalancer,
                                        "RoundRobinBalancer": self.RoundRobinBalancer,
                                        "WeightedRoundRobinBalancer": self.WeightedRoundRobinBalancer}
        
        self.balance_f = self.fs.get(name_f)
        if self.balance_f == None:
            print(f"Функция балансировки {name_f} не реализована")
            exit(1)
        
        if name_f == "WeightedRoundRobinBalancer" and srv_t == None:
            print("Для алгоритма балансировки WeightedRoundRobinBalancer в конфигурации системы надо ввести веса")
            exit(1)
        
        self.srv_i: dict[str, int] = {}
        print(srv_t)
        for s in srv_t:
            self.srv_i[s.name] = 0
        self.current_server_index = 0

    def test(self, task, pods: list[Pod]):
        if pods == []:
            return task, pods
        i = random.randint(0, len(pods) - 1)
        pods[i].add_task(task)
        return task, pods

    def LeastResponseTimeBalancer(self, task, pods: list[Pod]):
        if pods == []:
            return task, pods
        
        mi = -1
        ms = 10**10
        # print("-----------------------------------")
        for i in range(len(pods)):
            s = pods[i].responces_time_avg
            # print("Pods", i, " = ", s, "ms =", ms, "mi =", mi)
            if ms > s:
                mi = i
                ms = s
        # print("WIN mi =", mi)
        pods[mi].add_task(task)
        return task, pods

    def LeastConnectionsBalancer(self, task, pods: list[Pod]):
        if pods == []:
            return task, pods
        
        mi = -1
        ms = 10**10
        for i in range(len(pods)):
            s = len(pods[i].queue_tasks)
            if pods[i].is_blocked:
                s += 1

            if ms > s:
                mi = i
                ms = s
                
        pods[mi].add_task(task)
        
        return task, pods

    def RoundRobinBalancer(self, task, pods: list[Pod]):
        if pods == []:
            return task, pods
        
        pods[self.srv_i[pods[0].name]].add_task(task)
        
        
        self.srv_i[pods[0].name] = (self.srv_i[pods[0].name] + 1) % len(pods)
        
        
        return task, pods
    
    def WeightedRoundRobinBalancer(self, task, pods: list[Pod]):
        if pods == []:
            return task, pods
        
        total_weight = 0
        for p in pods:
            total_weight += p.weight
        
        rand_weight = random.randint(1, total_weight)
        current_weight = 0
        
        for i, p in enumerate(pods):
            current_weight += p.weight
            if current_weight >= rand_weight:
                pods[i].add_task(task)
                break
        
        
        return task, pods