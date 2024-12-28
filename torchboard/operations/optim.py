from typing import Any, Dict, Set, Tuple, Union
from torch.optim import Optimizer, Adam, SGD, Adagrad, Adadelta


class OptimizerOperator:
    def __init__(self, optimizer: Optimizer):
        self.optim = optimizer
        self.parameters: Set[str] = set()

    def get_parameters(self) -> Dict[str, type]:
        pass

    def update_parameters(self, parameter: str, value: Any):
        assert parameter in self.parameters, f"Parameter {
            parameter} not found in {self.optim.__class__.__name__}"
        setattr(self.optim, parameter, value)

    @staticmethod
    def get_optimizer(optimizer) -> "OptimizerOperator":
        """ Returns Optimizer operator for proper of optimizers """


a = Adam()


class AdamOperator(OptimizerOperator):
    def get_parameters(self):
        return {
            "lr": float,
            "betas": Tuple[float, float],
            "eps": float,
            "weight_decay": float,
            "amsgrad": bool,
        }

sgd = SGD()

class SGDOperator(OptimizerOperator):
    pass