from collections import defaultdict
from typing import Dict, List, Literal, Union
from torch.nn.modules.loss import _Loss
# from torchboard import Board


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
        last_change = {}
        for key, value in self.history.items():
            #TODO fix this
            if key in self.last_indexes and self.last_indexes[key] < len(value):
                last_change[key] = value[self.last_indexes[key]:]   
                self.last_indexes[key] = len(value)

        return last_change

    def get_all(self) -> _STRUCT:
        self.last_indexes = {key: len(value) for key, value in self.history.items()}
        return self.history
    

def overwrite_criterion_loss_update(criterion: _Loss, func: callable, board) -> _Loss:
    criterion.base_forward = criterion.forward
    def forward(*args, **kwargs):
        loss = criterion.base_forward(*args, **kwargs)
        if  board.model and  board.model.training:
            func(criterion_train=loss)
        else:
            func(criterion_eval=loss)
        return loss
    criterion.forward = forward    
    return criterion

