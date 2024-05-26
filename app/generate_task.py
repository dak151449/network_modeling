import numpy as np

from app.objects.task import Task

class generator():
    
    def __init__(self, handlers: list[int]):
        self.tasks: list[Task] = []
        pass
    
    # def generate_uniform_values(self):
    #     return np.linspace(start, end, num_values).tolist()