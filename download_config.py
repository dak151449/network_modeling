import yaml

from app.objects.service import Service, Handler


def download_config(name = "./configs/setup.yaml"):
    with open(name, 'r') as file:
        data = yaml.safe_load(file)
        print(data)
        return data

    
def get_services() -> list[list[Service], list[Handler], dict[str, int], int, str, int]:
    data = download_config()
    generator = data.get("generator")
    if generator is None:
        print("generator is None")
        exit(1)
        
    list_srvs = data.get("srvs")
    if list_srvs is None:
        print("srvs is None")
        exit(1)
    
    out_srvs: list[Service] = []
    handlers = []
    
    
    
    probability = 0
    hd_ids = []
    for srv in list_srvs:
        s, hs, h_ps = generate_srv(srv)
        out_srvs.append(s)
        handlers += hs
        probability += h_ps
        
        hd_ids += s.hendlers.keys()
    
    if len(hd_ids) != len(set(hd_ids)):
        print("Названия handler не должны совпадать!")
        exit(1)
        
                
    if abs(probability - 1.0) > 10**(-5):
        print("probability в сумме должно быть равно 1", abs(probability - 1.0))
        exit(1)
    
    m = data.get("model")
    if m is None:
        print("model не может быть пустой", "model is none")
        exit(1)
    stop_time = m.get("stop_time")
    if stop_time is None:
        print("stop_time не может быть пустое", stop_time)
        exit(1)
        
    check_handlers(out_srvs, hd_ids)
    
    return out_srvs, handlers, generator, data.get("balancer").get("max_length_queue_task"), data.get("balancer").get("function"), stop_time

def generate_srv(data) -> list[Service, dict[int, Handler], float]:
    handlers: dict[int, Handler] = {}
    hs = []
    h_ps = 0
    if data.get("handlers") is None:
        print("Handlers is None")
        exit(1)
        
    for h in data.get("handlers"):
        h_id = h.get("handler")
        if h_id is None:
            print("Handler is None")
            exit(1)
            
        h_time = h.get("time")
        if h_time is None:
            print("Time is None")
            exit(1)
            
        h_probability = h.get("probability")
        if h_probability is None:
            print("probability не должен быть пустым")
            exit(1)
        h_ps += h_probability
        h_way = []
        if h.get("way") != None:
            h_way =  h.get("way")
            
        handler = Handler(h_id, h_time, h_way, h_probability)
        if handlers.get(h_id) != None:
            print("Названия handler не должны совпадать!")
            exit(1)
        
        handlers[h_id] = handler
        hs.append(handler)
    print("count_pods:", data.get("count_pods"))
    
    
    p_w = data.get("pods_weight")
    pods_count = data.get("count_pods")
    if pods_count == None or (p_w !=None and len(p_w) != pods_count):
        print("pods_count должно совпадать с количество элементов в pods_weight")
        exit(1)
    
    max_length_queue_task = data.get("max_length_queue_task")
    if max_length_queue_task == None:
        max_length_queue_task = 100
        print("max_length_queue_task не задана => значение по дефолту 100")
    
    return Service(data.get("service_name"), handlers, max_length_queue_task, pods_count, p_w), hs, h_ps

def check_handlers(srvs: list[Service], handlers_ids: list[any]):
    for s in srvs:
        for h_id in s.hendlers:
            for w in s.hendlers[h_id].way:
                if w not in handlers_ids or w == h_id:
                    print("Путь указан либо в несуществующий handler, либо сам в себя, что недопускается")
                    exit(1)