import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from app.objects.model import Model
from app.global_constants import const




def print_stats(model: Model, event_types):
    print("STATS")
    for i in model.balancer.srvs:
        ps = model.balancer.srvs[i]
        print('Сервис', i)
        plt.figure()
        number_pod = 1
        for p in ps.pods:
            lb = number_pod
            print("POD_ID:", p.id)
            # print("Количество задач в очереди:", p.count_task_int_deque)
            # print("Rps:", p.rps)
            # Создание графика
            
            x = range(len(p.rps))
            plt.plot(p.rps, label=str(number_pod))#,linestyle='-', marker='o')
            # plt.plot(p.service.rps, label='y = 5 - x', linestyle='--', marker='x')
            # plt.plot(p.service.rps, label='y = 2', linestyle='-.', marker='s')
            number_pod += 1
        # Добавление заголовков и меток
        plt.title('Количество обрабатываемых транзакций за единицу времени у сервиса ' + i)
        plt.xlabel('время')
        plt.ylabel('колимчество транзакций')

        # Отображение легенды
        plt.legend()

        # Показ графика
        plt.grid(True)
        plt.show()
        
    print("COUNT_QUE")
    for i in model.balancer.srvs:
        ps = model.balancer.srvs[i]
        print('Сервис', i)
        plt.figure()
        number_pod = 1
        for p in ps.pods:
            lb = number_pod
            print("POD_ID:", p.id)
            # print("Количество задач в очереди:", p.count_task_int_deque)
            # print("Rps:", p.rps)
            # Создание графика
            
            plt.plot(p.count_task_int_deque, label=str(number_pod))

            number_pod += 1
        # Добавление заголовков и меток
        plt.title('Длинна очереди с течением времени сервиса ' + i)
        plt.xlabel('время')
        plt.ylabel('количество задач в очереди')

        # Отображение легенды
        plt.legend()

        # Показ графика
        plt.grid(True)
        plt.show()



def print_global_stat(model: Model, event_types):
    """Вывод общих метрик

    Args:
        model (Model): _description_
    """
    print_s()
    System_all_task(model)
    print_s()
    System_performance(model)
    print_s()
    Number_of_transactions_serviced(model)
    print_s()
    Average_time_spent_in_system(model, event_types)
    print_s()
    Average_waiting_time_in_srv_queue(model, event_types)
    print_s()
    Average_waiting_time_in_balancer_queue(model, event_types)
    print_s()
    Average_queue_length_in_balancer(model)
    print_s()
    Average_queue_length_in_srv(model)
    print_s()
    Busy_time(model)
    print_s()
    Idle_time(model)
    print_s()
    Count_task_canceled_in_model(model)
    print_s()
    Count_task_canceled(model)
    print_s()
    Count_task_balancer_canceled(model)
    print_s()
    return

def System_all_task(model: Model):
    print(f"Всего сгенерировано {const.all_task_count} задач.")
    s = 0
    for t in model.balancer.tx_stats_count:
        s += model.balancer.tx_stats_count_canceled[t]
    
    if s != 0:
        print(f"Потеряно {(s/const.all_task_count)*100}%")

def Number_of_transactions_serviced(model: Model):
    c = 0
    for t in model.balancer.tx_stats_count:
        c += model.balancer.tx_stats_count[t]
        
    print("Количество обслуженных транзакций:", c)
    print("    Общее количество транзакций (единиц работы), которые прошли через систему или её отдельные компоненты.")
    return

def Average_time_spent_in_system(model: Model, event_types):
    for t in model.balancer.tx_stats_count:
        if model.balancer.tx_stats_count[t] == 0:
            print(f"Среднее время пребывания в системе транзакции типа {t}:",0)
        else:
            print(f"Среднее время пребывания в системе транзакции типа {t}:",model.balancer.tx_stats_time[t] / model.balancer.tx_stats_count[t])
        
        
    
def Average_waiting_time_in_srv_queue(model: Model, event_types):
    for srv in model.balancer.srvs:
        s = 0
        for p in model.balancer.srvs[srv].pods:
            if p.res_count != 0:
                s += p.waiting_time_in_srv_queue / p.res_count
        
        print(f"Среднее время ожидания в очереди сервиса транзакции типа {srv}:", s / len(model.balancer.srvs[srv].pods))
        
def Average_waiting_time_in_balancer_queue(model: Model, event_types):
    for t in model.balancer.tx_stats_count:
        print(f"Среднее время ожидания в очереди балансировщика транзакции типа {t}:",model.balancer.tx_stats_balance_time[t])
        
def Average_queue_length_in_balancer(model: Model):
    # model.balancer.
    # todo
    pass
    
def Average_queue_length_in_srv(model: Model):
    # model.balancer.
    # todo
    
    for s in model.balancer.srvs:
        print(f"Средняя длина очереди сервиса {s}:")
        tab = "    "
        pi = 0
        for p in model.balancer.srvs[s].pods:
            print(tab, f"Образ {pi}:", int(np.average(p.count_task_int_deque)))
            pi += 1

def System_performance(model: Model):
    c = 0
    for t in model.balancer.tx_stats_count:
        c += model.balancer.tx_stats_count[t]
    
    print("Производительность системы:", c / const.STOP_TIME)
    return

def Busy_time(model: Model):
    for s in model.balancer.srvs:
        print(f"Общее время в процентах, в течение которого устройство {s} было занято обслуживанием транзакций:")
        tab = "    "
        pi = 0
        for p in model.balancer.srvs[s].pods:
            print(tab, f"Образ {pi}: {(p.busy_time / const.global_time) * 100}%")
            pi += 1
    return

def Idle_time(model: Model):
    for s in model.balancer.srvs:
        print(f"Общее время в процентах, в течение которого устройство {s} простаивало, то есть не выполняло никаких задач:")
        tab = "    "
        pi = 0
        for p in model.balancer.srvs[s].pods:
            print(tab, f"Образ {pi}: {(p.idle_time / const.global_time) * 100}%")
            pi += 1
    return

def Count_task_canceled_in_model(model: Model):
    for t in model.balancer.tx_stats_count:
        print(f"Общее количество отмененных транзакций типа {t}:",model.balancer.tx_stats_count_canceled[t])
 
def Count_task_balancer_canceled(model: Model):
    print(f"Общее количество отмененных транзакций балансировщиком:")
    for s in model.balancer_count_canceled:
        tab = "    "
        print(tab, f"Тип {s}: {model.balancer_count_canceled[s]}")
    return
        
def Count_task_canceled(model: Model):
    for s in model.balancer.srvs:
        print(f"Общее количество отмененных транзакций у сервиса {s}:")
        tab = "    "
        pi = 0
        for p in model.balancer.srvs[s].pods:
            print(tab, f"Образ {pi}: {p.count_task_canceled}")
            pi += 1

def print_s():
    print("--------------------------------------------------")
    return