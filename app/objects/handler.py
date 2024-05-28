

class Handler:
    # id: int = 0 
    # """уникальный номер хендлера, задается пользователем в конфиге"""
    # local_time: int = 0
    # """время нужное хендлеру для выполнения внутренних действий, задается пользователем в конфиге"""
    # way: list[int] = [] ## 
    # """список последовтельных вызовов других ручек (опционально подумать про local_time)
    # """

    def __init__(self, id: int, t: int, way: list[int], probability) -> None:
        self.id: int = id
        self.local_time: int = t
        self.way: list[int] = way
        self.probability = probability
        
    def __str__(self) -> str:
        return f"Handler id: {self.id}, local_time: {self.local_time}, way: {self.way}"
