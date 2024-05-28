import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from app.objects.model import Model





def print_stats(model: Model):
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

