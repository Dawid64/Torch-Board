from torch.nn import Module


class ModelOperator:
    def __init__(self, model: Module):
        self.model = model

    def get_current_device(self):
        return next(iter(self.model.parameters())).device
