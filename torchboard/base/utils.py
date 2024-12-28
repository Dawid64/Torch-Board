from collections import defaultdict
from typing import Dict, List, Literal, Union


_SUPPORTED = Literal['Model', 'Optimizer', 'List', 'Value']
_RESPONSE = Dict[str, Union[int, float]]

class History:
    def __init__(self):
        self.history: Dict[str, List[Union[int,float]]] = defaultdict(list) 
        self.last_indexes: Dict[str, int] = defaultdict(int)


    def update(self, val: _RESPONSE) -> None:
        for variable, value in val.items():
            self.history[variable].append(value)

    def get_last(self) -> _RESPONSE:
        """
        Get last value of each variable 
        Ff there will be no change and get last is called again it will return the same variable 
        """
        return {key: value[-1] for key,value in self.history.items()}

    def get_since_last_change(self) -> List[_RESPONSE]:
        """
        Get all values that changed since last get as dict of lists 
        """
        return {key: value[self.last_indexes[key]:] for key, value in self.history.items() if self.last_indexes[key] < len(value)}

    def get_all(self) -> List[_RESPONSE]:
        self.last_indexes = {key: len(value) for key, value in self.history.items()}
        return self.history
