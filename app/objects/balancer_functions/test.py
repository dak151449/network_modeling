import random

from app.objects.pod import Pod





def test(task, pods: list[Pod]):
    if pods == []:
        return task, pods
    i = random.randint(0, len(pods) - 1)
    pods[i].add_task(task)
    return task, pods

def LeastResponseTimeBalancer(task, pods: list[Pod]):
    if pods == []:
        return task, pods
    
    mi = -1
    ms = 10**10
    for i in range(len(pods)):
        s = []
        for r in pods[i].responces:
            s.append(r.end_global_time - r.start_global_time)

        print("LeastResponseTimeBalancer:", pods[i].name, "+++++++++++++++ ", s ," +++++++++++++++++")
        if len(s) == 0:
            s = [0]
        
        if ms > min(s) :
            mi = i
            ms = min(s)
            
    pods[mi].add_task(task)
    
    return task, pods