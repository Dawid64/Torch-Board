from typing import Any, List
class Listener:
    """
    Class for extracting data from pytorch and preparing it for backend
    """
    def __init__(self):
        self.history = []
        self.last_get_index = 0
    
    def add(self, value: Any):
        self.history.append(value)

    def get(self) -> List[Any]:
        history_part = self.history[self.last_get_index:]
        self.last_get_index = len(self.history)
        return history_part
    
    def get_all(self) -> List[Any]:
        return self.history
