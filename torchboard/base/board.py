from typing import Any, Dict, List, Optional, Union
import torch
from torch.nn import Module
from torch.optim import Optimizer
from .utils import _SUPPORTED, History, overwrite_criterion_loss_update
from torchboard.operations.optim import OptimizerOperator
from torch.nn.modules.loss import _Loss



# TODO: Add documentation
class Board:
    """
    
    
    """
    def __init__(self):
        self.model: Optional[Module]
        self.optim: Optional[Optimizer]
        self.criterion: Optional[_Loss]
        self.history: History = History()
        self.operators: Dict[str, Any] = {}

    def update(self, **kwargs):
        """ Update arguments """

        parsed = self._argument_parser(kwargs)
        changes = {arg_name: float(kwargs[arg_name])
                   for arg_name, arg_type in parsed.items() if arg_type in ['Value']}
        self.history.update(changes)

    def _argument_parser(self, kwargs: Dict[str, Any]) -> Dict[str, _SUPPORTED]:
        parsed: Dict[str, _SUPPORTED] = {arg_name: Board._match_argument(
            arg) for arg_name, arg in kwargs.items()}
        reverse_parsing: Dict[_SUPPORTED, Any] = {Board._match_argument(
            arg): kwargs[arg_name] for arg_name, arg in kwargs.items()}
        if 'Optimizer' in reverse_parsing:
            optim = reverse_parsing['Optimizer']
            optim_operator = OptimizerOperator.get_optimizer(optim)
            self.operators['Optimizer'] = optim_operator
            self.optim = optim
        if 'Model' in reverse_parsing:
            model = reverse_parsing['Model']
            self.model = model
        if 'Criterion' in reverse_parsing:
            criterion = reverse_parsing['Criterion']
            self.criterion = overwrite_criterion_loss_update(criterion, self.update, self)
        return parsed

    @staticmethod
    def _match_argument(argument: Any) -> _SUPPORTED:
        if isinstance(argument, _Loss):
            return 'Criterion'
        if isinstance(argument, Module):
            return 'Model'
        elif isinstance(argument, Optimizer):
            return 'Optimizer'
        elif isinstance(argument, List):
            return 'List'
        elif isinstance(argument, Union[int, float,torch.Tensor]):
            return 'Value'
        else:
            raise NotImplementedError(
                f'There is currently no support for: {argument.__class__}')
