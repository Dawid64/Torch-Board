from torch.nn import Module
from torch import nn
import torch
import numpy as np
import torchvision
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use("Agg")


class ModelOperator:
    def __init__(self, model: Module):
        self.model = model
        self.cache = None

    def get_current_device(self):
        return next(iter(self.model.parameters())).device

    def get_layers(self):
        modules = []
        for name, module in self.model.named_children():
            modules.append((name, module))
        return modules

    def get_parameters(self):
        params = []
        for name, param in self.model.named_parameters():
            params.append((name, param))
        return params

    def get_module_by_name(self, module_name: str):
        return getattr(self.model, module_name)

    def register_forward_hooks(self, module_name: str, output_num: int = 0):
        module = self.get_module_by_name(module_name)

        def forward_hook(module, input, output):
            self.cache = output[output_num]
            handle.remove()

        handle = module.register_forward_hook(forward_hook)

    def register_backward_hooks(self, module_name: str, output_num: int = 0):
        module = self.get_module_by_name(module_name)

        def backward_hook(module, grad_input, grad_output):
            self.cache = grad_output[output_num]
            handle.remove()

        handle = module.register_backward_hook(backward_hook)
