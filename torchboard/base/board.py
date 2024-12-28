from typing import Any, Dict, List, Literal, Optional, Union
from torch.nn import Module
from torch.optim import Optimizer

_SUPPORTED = Literal['Model', 'Optimizer', 'List', 'Value']
_RESPONSE = Dict[str, Union[int, float]]

# TODO: Add documentation
class Board:
    """
    
    
    """
    def __init__(self):
        self.model: Optional[Module]
        self.optim: Optional[Optimizer]
        self.history: List[_RESPONSE]

    def update(self, **kwargs):
        """ Update arguments """
        parsed = self._argument_parser(kwargs)
        changes = {arg_name: kwargs[arg_name]
                   for arg_name, arg_type in parsed.items() if arg_type in ['Value']}
        self.history.append(changes)

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
        elif isinstance(argument, Union[int, float]):
            return 'Value'

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
