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
        plt.title('RPS сервиса ' + i)
        plt.xlabel('time')
        plt.ylabel('rps')

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
        plt.title('COUNT_QUE сервиса ' + i)
        plt.xlabel('time')
        plt.ylabel('count task')

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
    System_performance(model)
    
    Number_of_transactions_serviced(model)
    Average_time_spent_in_system(model, event_types)
    
    Average_waiting_time_in_srv_queue(model, event_types)
    Average_waiting_time_in_balancer_queue(model, event_types)
    
    Average_queue_length_in_balancer(model)
    
    Average_queue_length_in_srv(model)
    return


def Number_of_transactions_serviced(model: Model):
    
    print("Количество обслуженных транзакций:", len(const.closed_tasks) + len(const.subtask_closed))
    print("    Общее количество транзакций (единиц работы), которые прошли через систему или её отдельные компоненты.")
    return

def Average_time_spent_in_system(model: Model, event_types):
    txs = const.closed_tasks + const.subtask_closed
    
    
    for id in event_types:
        s = 0
        for t in txs:
            if t.handler_id == id:
                s += (t.end_global_time - t.start_global_time)
        
        print(f"Среднее время пребывания в системе транзакции типа {id}:", s / len(txs))
        
    
def Average_waiting_time_in_srv_queue(model: Model, event_types):
    txs = const.closed_tasks + const.subtask_closed
    
    
    for id in event_types:
        s = 0
        si = 0
        for t in txs:
            if t.handler_id == id:
                s += (t.end_time_in_pod_que - t.start_time_in_pod_que)
                si += 1
        
        print(f"Среднее время ожидания в очереди сервиса транзакции типа {id}:", s / si)
        
def Average_waiting_time_in_balancer_queue(model: Model, event_types):
    txs = const.closed_tasks + const.subtask_closed
    
    
    for id in event_types:
        s = 0
        si = 0
        for t in txs:
            if t.handler_id == id:
                s += (t.end_time_in_balancer_que - t.start_time_in_balancer_que)
                si += 1
        
        print(f"Среднее время ожидания в очереди балансировщика транзакции типа {id}:", s / si)
        
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
            print(tab, f"Образ {pi}:", np.average(p.count_task_int_deque))
            pi += 1

def System_performance(model: Model):
    print("Производительность системы:", (len(const.closed_tasks) + len(const.subtask_closed))/ const.STOP_TIME)
    return