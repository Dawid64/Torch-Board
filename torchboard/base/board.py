from typing import Any, Dict, List, Optional, Union
import torch
from torch.nn import Module
from torch.optim import Optimizer
from .utils import _SUPPORTED, History


# TODO: Add documentation
class Board:
    """
    
    
    """

    def __init__(self):
        self.model: Optional[Module]
        self.optim: Optional[Optimizer]
        self.history: History = History()

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
            arg): arg_name for arg_name, arg in kwargs.items()}
        optim = parsed[reverse_parsing['Optimizer']]
        model = parsed[reverse_parsing['Model']]
        self.model = model
        self.optim = optim
        return parsed

    @staticmethod
    def _match_argument(argument: Any) -> _SUPPORTED:
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
