from typing import Dict, List, Literal, Union
from torch.nn.modules.loss import _Loss
# from torchboard import Board


_SUPPORTED = Literal['Model', 'Optimizer', 'List', 'Value']
_RESPONSE = Dict[str, Union[int, float]]

class History:
    def __init__(self):
        self.history: List[_RESPONSE] = []
        
    def update(self, value: _RESPONSE):
        self.history.append(value)

    def get_last(self) -> _RESPONSE:
        self.last_get_index = len(self.history)
        return self.history[-1]

    def get_since_last_change(self) -> List[_RESPONSE]:
        history_part = self.history[self.last_get_index:]
        self.last_get_index = len(self.history)
        return history_part

    def get_all(self) -> List[_RESPONSE]:
        self.last_get_index = len(self.history)
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

