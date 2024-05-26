import yaml

from app.objects.service import Service, Handler


def download_config(name = "./configs/setup.yaml"):
    with open(name, 'r') as file:
        data = yaml.safe_load(file)
        return data

    
def get_services() -> list[Service]:
    srv = download_config()
    list_srvs = srv.get("srvs")
    
    out_srvs: list[Service] = []
    
    for srv in list_srvs:
        out_srvs.append(generate_srv(srv))
    
    return out_srvs

def generate_srv(data) -> Service:
    handlers: dict[int, Handler] = {}
    
    for h in data.get("handlers"):
        h_id = h.get("handler")
        h_time = h.get("time")
        h_way = []
        if h.get("way") != None:
            h_way =  h.get("way")
            
        handler = Handler(h_id, h_time, h_way)
        handlers[h_id] = handler
    print("count_pods:", data.get("count_pods"))
    return Service(data.get("service_name"), handlers, int(str(data.get("count_pods"))))