import yaml

from app.objects.service import Service, Handler


def download_config(name = "./configs/setup.yaml"):
    with open(name, 'r') as file:
        data = yaml.safe_load(file)
        print(data)
        return data

    
def get_services() -> list[list[Service], list[Handler], dict[str, int]]:
    data = download_config()
    generator = data.get("generator")
    
    list_srvs = data.get("srvs")
    
    out_srvs: list[Service] = []
    handlers = []
    
    probability = 0
    
    for srv in list_srvs:
        s, hs, h_ps = generate_srv(srv)
        out_srvs.append(s)
        handlers += hs
        probability += h_ps
        
    if abs(probability - 1.0) > 10**(-5):
        print("probability в сумме должно быть равно 1", abs(probability - 1.0))
        exit(1)
        
    return out_srvs, handlers, generator, data.get("balancer").get("max_length_queue_task"), data.get("balancer").get("function")

def generate_srv(data) -> list[Service, dict[int, Handler], float]:
    handlers: dict[int, Handler] = {}
    hs = []
    h_ps = 0
    for h in data.get("handlers"):
        h_id = h.get("handler")
        h_time = h.get("time")
        h_probability = h.get("probability")
        if h_probability is None:
            print("probability не должен быть пустым")
            exit(1)
        h_ps += h_probability
        h_way = []
        if h.get("way") != None:
            h_way =  h.get("way")
            
        handler = Handler(h_id, h_time, h_way, h_probability)
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