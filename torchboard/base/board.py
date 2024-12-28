from typing import Any, Dict, List, Optional, Union
from torch.nn import Module
from torch.optim import Optimizer
from .utils import _SUPPORTED, History
from torchboard.operations.optim import OptimizerOperator

# TODO: Add documentation
class Board:
    """
    
    
    """

    def __init__(self):
        self.model: Optional[Module]
        self.optim: Optional[Optimizer]
        self.history: History = History()
        self.operators: Dict[str, Any] = {}

    def update(self, **kwargs):
        """ Update arguments """
        parsed = self._argument_parser(kwargs)
        changes = {arg_name: kwargs[arg_name]
                   for arg_name, arg_type in parsed.items() if arg_type in ['Value']}
        self.history.update(changes)

    def _argument_parser(self, kwargs: Dict[str, Any]) -> Dict[str, _SUPPORTED]:
        parsed: Dict[str, _SUPPORTED] = {arg_name: Board._match_argument(
            arg) for arg_name, arg in kwargs.items()}
        reverse_parsing: Dict[_SUPPORTED, Any] = {Board._match_argument(
            arg): arg_name for arg_name, arg in kwargs.items()}
        if 'Optimizer' in parsed:
            optim = parsed[reverse_parsing['Optimizer']]
            optim_operator = OptimizerOperator.get_optimizer(optim)
            self.operators['Optimizer'] = optim_operator
        if 'Model' in parsed:
            model = parsed[reverse_parsing['Model']]
            self.model = model
        return parsed

    @staticmethod
    def _match_argument(argument: Any) -> _SUPPORTED:
        if isinstance(argument, Module):
            return 'Model'
        elif isinstance(argument, Optimizer):
            return 'Optimizer'
        elif isinstance(argument, List):
            return 'List'
        elif isinstance(argument, Union[int, float]):
            return 'Value'
        else:
            raise NotImplementedError(
                f'There is currently no support for: {argument.__class__}')
