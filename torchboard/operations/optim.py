from typing import Any, Dict, Set, Tuple
from torch.optim import Optimizer


class OptimizerOperator:
    def __init__(self, optimizer: Optimizer):
        self.optim = optimizer
        self.parameters: Set[str] = set(self.get_parameters().keys())

    def get_parameters(self) -> Dict[str, type]:
        raise NotImplementedError("Optimizer not selected")
    
    def get_current_parameters(self) -> Dict[str, Any]:
        return {k: self.optim.param_groups[0][k] for k in self.get_parameters()}

    def update_parameters(self, parameter: str, value: Any):
        assert parameter in self.parameters, f"Parameter {parameter} not found in {self.optim.__class__.__name__}"
        for group in self.optim.param_groups:
            group[parameter] = value

    def get_parameter_value(self, parameter: str) -> Any:
        return self.optim.param_groups[0][parameter]

    @staticmethod
    def get_optimizer(optimizer) -> "OptimizerOperator":
        """ Returns Optimizer operator for proper of optimizers """
        if optimizer.__class__.__name__ not in __OPTIMIZERS__:
            raise NotImplementedError(
                f"Optimizer {optimizer} not supported")
        return __OPTIMIZERS__[optimizer.__class__.__name__](optimizer)


class AdamOperator(OptimizerOperator):
    def get_parameters(self):
        return {
            "lr": float,
            "betas": Tuple[float, float],
            "eps": float,
            "weight_decay": float,
            "amsgrad": bool,
        }


class SGDOperator(OptimizerOperator):
    def get_parameters(self):
        return {
            "lr": float,
            "momentum": float,
            "dampening": float,
            "weight_decay": float,
            "nesterov": bool
        }


class AdagradOperator(OptimizerOperator):
    def get_parameters(self):
        return {
            "lr": float,
            "lr_decay": float,
            "weight_decay": float,
            "initial_accumulator_value": float,
            "eps": float,
            "foreach": bool,
        }


class AdadeltaOperator(OptimizerOperator):
    def get_parameters(self):
        return {
            "lr": float,
            "rho": float,
            "eps": float,
            "weight_decay": float,
            "foreach": bool,
        }

__OPTIMIZERS__ = {
    'Adam': AdamOperator,
    'SGD': SGDOperator,
    'Adagrad': AdagradOperator,
    'Adadelta': AdadeltaOperator
}
