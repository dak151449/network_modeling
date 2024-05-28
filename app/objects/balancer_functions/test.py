import random

from app.objects.pod import Pod


class Func_balancer:
    def __init__(self, name_f):
        self.fs: dict[str, function] = {"test": self.test, "LeastResponseTimeBalancer": self.LeastResponseTimeBalancer,
                                        "LeastConnectionsBalancer": self.LeastConnectionsBalancer}
        
        self.balance_f = self.fs[name_f]
        # self.servers = servers
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
        for i in range(len(pods)):
            s = pods[i].responces_time_avg

            if ms > s:
                mi = i
                ms = s
                
        pods[mi].add_task(task)
        
        return task, pods

    def LeastConnectionsBalancer(self, task, pods: list[Pod]):
        if pods == []:
            return task, pods
        
        mi = -1
        ms = 10**10
        for i in range(len(pods)):
            s = len(pods[i].queue_tasks)

            if ms > s:
                mi = i
                ms = s
                
        pods[mi].add_task(task)
        
        return task, pods

    def balance(self):
        current_server = self.servers[self.current_server_index]
        self.current_server_index = (self.current_server_index + 1) % len(self.servers)
        
        return current_server