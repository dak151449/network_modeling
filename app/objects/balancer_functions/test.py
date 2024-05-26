from app.objects.pod import Pod





def test(task, pods: list[Pod]):
    if pods == []:
        return task, pods
    pods[0].add_task(task)
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

        print(pods[i].name, "+++++++++++++++ ", s ," +++++++++++++++++")
        if  len(s) == 0 or ms > min(s) :
            mi = i
            if s != []:
                ms = min(s)
            
    pods[mi].add_task(task)
    
    return task, pods