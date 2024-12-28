from collections import defaultdict
from typing import Dict, List, Literal, Union


_SUPPORTED = Literal['Model', 'Optimizer', 'List', 'Value']
_STRUCT = Dict[str, List[Union[int,float]]]

class History:
    def __init__(self):
        self.history: Dict[str, List[Union[int,float]]] = defaultdict(list) 
        self.last_indexes: Dict[str, int] = defaultdict(int)


    def update(self, val: Dict[str, Union[int,float]]) -> None:
        for variable, value in val.items():
            self.history[variable].append(value)

    def get_last(self) -> Dict[str, float]:
        """
        Get last value of each variable 
        Ff there will be no change and get last is called again it will return the same variable 
        """
        return {key: value[-1] for key,value in self.history.items()}

    def get_since_last_change(self) -> _STRUCT:
        """
        Get all values that changed since last get as dict of lists 
        """
        return {key: value[self.last_indexes[key]:] for key, value in self.history.items() if self.last_indexes[key] < len(value)}

    def get_all(self) -> _STRUCT:
        self.last_indexes = {key: len(value) for key, value in self.history.items()}
        return self.history
