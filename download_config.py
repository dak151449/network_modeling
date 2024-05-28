import yaml

from app.objects.service import Service, Handler


def download_config(name = "./configs/setup.yaml"):
    with open(name, 'r') as file:
        data = yaml.safe_load(file)
        return data

    
def get_services() -> list[list[Service], list[Handler], dict[str, int]]:
    srv = download_config()
    generator = srv.get("generator")
    
    list_srvs = srv.get("srvs")
    
    out_srvs: list[Service] = []
    handlers = []
    
    for srv in list_srvs:
        s, hs = generate_srv(srv)
        out_srvs.append(s)
        handlers += hs
    return out_srvs, handlers, generator

def generate_srv(data) -> Service:
    handlers: dict[int, Handler] = {}
    hs = []
    for h in data.get("handlers"):
        h_id = h.get("handler")
        h_time = h.get("time")
        h_probability = h.get("probability")
        h_way = []
        if h.get("way") != None:
            h_way =  h.get("way")
            
        handler = Handler(h_id, h_time, h_way, h_probability)
        handlers[h_id] = handler
        hs.append(handler)
    print("count_pods:", data.get("count_pods"))
    return Service(data.get("service_name"), handlers, int(str(data.get("count_pods")))), hs