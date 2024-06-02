class Task:
    def __init__(self, id: str, handler_id: int, global_time: int) -> None:
        self.id = id
        """название задачи"""
        self.handler_id = handler_id
        """id ручки те её уникальный номер среди всех ручек"""
        self.stack_service: int = -1
        """id ручки, которая порадила задачу или пользователь"""
    
        self.in_work: bool = False
        self.is_closed: bool = False
        self.is_canceled: bool = False
        
        self.start_global_time: int = global_time
        self.end_global_time: int = -1
        
        self.start_time_in_balancer_que: int = global_time
        self.end_time_in_balancer_que: int = -1
        
        self.start_time_in_pod_que: int = -1
        self.end_time_in_pod_que: int = -1
        
        self.start_work_time: int = -1
        self.end_work_time: int = -1
    
    def __str__(self) -> str:
        
        s = f'''
        id: {self.id}, handler_id: {self.handler_id}, stack_service: {self.stack_service}

            IN_WORK = {self.in_work}
            IS_CLOSE = {self.is_closed}
            
            END_WORK_GLOBAL_TIME = {self.end_global_time}
            START_GLOBAL_TIME = {self.start_global_time}
            
            WORK_GLOBAL_TIME = {self.end_global_time - self.start_global_time}
            TIME_IN_BALANCE_QUE = {self.end_time_in_balancer_que - self.start_time_in_balancer_que}
            TIME_IN_POD_QUE = {self.end_time_in_pod_que - self.start_time_in_pod_que}
            TIME_IN_WORK = {self.end_work_time - self.start_work_time}
        '''
        
        
        return s