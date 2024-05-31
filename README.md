# network_modeling
Simulates network operation to analyze balancing algorithms

Программа для анализа и моделирования работы алгоритмов балансировки. В конце работы приводит статистику обработки транзакций моделью, которая задается в конфигурационном файле. 



# Установка и запуск
```cmd
python --version >= 3.9

>> sudo apt install python3.9

>> python3.9 -m pip install numpy
>> python3.9 -m pip install pandas
>> python3.9 -m pip install matplotlib


# для запуска в корне проекта
>> python3.9 main.py
```

# Конфигурационный файл configs/setup.yaml

## Модель

- **model.stop_time**: Время остановки модели. Значение: `100000`.

## Балансировщик

- **balancer.max_length_queue_task**: Максимальная длина очереди задач. Значение: `100`.
- **balancer.function**: Функция балансировки. Используется `WeightedRoundRobinBalancer`.

## Сервисы

### Сервис A

- **service_name**: Имя сервиса. Значение: `A`.
- **pods_weight**: Веса подов сервиса. Список из 12 элементов, каждый равен `1`.
- **count_pods**: Количество образов. Значение: `12`.
- **max_length_queue_task**: Максимальная длина очереди задач для всех образов данного сервиса. Значение: `100`.

#### Обработчики

- **handler**: Идентификатор обработчика.
- **probability**: Вероятность выбора обработчика на стадии генерации задачи. Значение: `0.25`, те с вероятностью 25% сгенерируется новая задача для данного обработчика.
- **time**: Время обработки задач. Значение: `50`.
- **way**: Маршрут обработки (может отсутствовать). Значение: `[3, 2]` для первого обработчика. Значит, что задача создаст подзадачи и отправит их обработчику 3, а потом 2


### Генератор
- **generator.interval**: Интервал генерации задач. Значение: 200.
- **generator.count_in_iteration**: Количество задач за итерацию. Значение: 20.

Пример:

```yaml
model:
  stop_time: 100000
balancer:
  max_length_queue_task: 100
  function: WeightedRoundRobinBalancer
srvs:
  - service_name: A
    pods_weight: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    count_pods: 12
    max_length_queue_task: 100
    handlers:
      - handler: 1
        probability: 0.25
        time: 50
        way: [3, 2]
      - handler: 2
        probability: 0.25
        time: 50
  
  - service_name: B
    pods_weight: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    weight: 1
    count_pods: 12
    max_length_queue_task: 100
    handlers:
      - handler: 3
        probability: 0.25
        time: 50
      - handler: 4
        probability: 0.25
        time: 50
generator:
  interval: 200
  count_in_iteration: 20

Этот файл описывает конфигурацию модели, включающей в себя балансировщик, два сервиса с подами и обработчиками задач, а также генератор задач.
```

### Набор алгоритмов балансировки для конфигурации

 - **test**
 - **LeastResponseTimeBalancer**
 - **LeastConnectionsBalancer**
 - **RoundRobinBalancer**
 - **WeightedRoundRobinBalancer**
