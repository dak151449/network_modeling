


class Task:
    def __init__(self, id: str, handler_id: int) -> None:
        self.id = id
        """название задачи"""
        self.handler_id = handler_id
        """id ручки те её уникальный номер среди всех ручек"""
        self.stack_service: int = -1
        """id ручки, которая порадила задачу или пользователь"""
    
        self.in_work: bool = False
        self.is_closed: bool = False
        self.start_global_time: int = -1
        self.end_global_time: int = -1
    
    def __str__(self) -> str:
        return f'id: {self.id}, handler_id: {self.handler_id}, stack_service: {self.stack_service}'

    def add_service_to_stack(self, service_id) -> None:
        """Задает stack_service 

        Args:
            service_id (_type_): id сервиса (пода) от которого пришла задача
        """
        self.stack_service = service_id

    def pop_service_id_from_stack(self) -> int:
        """возвращает и сбрасывает id пода родителя taski

        Returns:
            int: id пода родителя taski 
        """
        out = self.stack_service 
        self.stack_service = -1 # сбрасываем на всякий случай
        return out
