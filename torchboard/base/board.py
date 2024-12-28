from typing import Any, Dict, List, Optional, Union
import torch
from torch.nn import Module
from torch.optim import Optimizer
from .utils import _SUPPORTED, History
from torchboard.operations.optim import OptimizerOperator
from torchboard.server.torchboard_server import TorchBoardServer

# TODO: Add documentation
class Board:
    """
    
    
    """
    def __init__(self):
        self.model: Optional[Module]
        self.optim: Optional[Optimizer]
        self.history: History = History()
        self.operators: Dict[str, Any] = {}
        
        self.server = TorchBoardServer(board=self)
        self.server.start()
        
        self.do_training = True

    def update(self, **kwargs):
        """ Update arguments """
        parsed = self._argument_parser(kwargs)
        
        listener_changes = {arg_name: float(kwargs[arg_name])
                   for arg_name, arg_type in parsed.items() if arg_type in ['Value']}
        
        if len(listener_changes) > 0:
            self.history.update(listener_changes)
        
        while not self.do_training:
            pass #Is this the best way to do this?        
        
    def update_variable(self, name: str, value: Any):
        if name.startswith('optim_'):
            self.operators['Optimizer'].update_parameters(name[6:], value)
        self.server.update_changeable_value(name, value)
        #TODO update other variables
    
    def toggle_training(self):
        self.do_training = not self.do_training
        
    def save_model(self):
        torch.save(self.model, 'model.pth')

    def _argument_parser(self, kwargs: Dict[str, Any]) -> Dict[str, _SUPPORTED]:
        parsed: Dict[str, _SUPPORTED] = {arg_name: Board._match_argument(
            arg) for arg_name, arg in kwargs.items()}
        reverse_parsing: Dict[_SUPPORTED, Any] = {Board._match_argument(
            arg): kwargs[arg_name] for arg_name, arg in kwargs.items()}
        if 'Optimizer' in reverse_parsing:
            optim = reverse_parsing['Optimizer']
            optim_operator = OptimizerOperator.get_optimizer(optim)
            
            for k in optim_operator.get_parameters().keys():
                optim_value = optim.param_groups[0][k] #grab set value from optimizer
                self.server.register_changeable_value(f"optim_{k}", optim_value)
            
            self.operators['Optimizer'] = optim_operator
            self.optim = optim
        if 'Model' in reverse_parsing:
            model = reverse_parsing['Model']
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
        elif isinstance(argument, Union[int, float,torch.Tensor]):
            return 'Value'
        else:
            raise NotImplementedError(
                f'There is currently no support for: {argument.__class__}')
            
    def __del__(self):
        self.server.stop()