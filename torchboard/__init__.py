"""
Torchboard is a simple and easy-to-use library for visualizing PyTorch model's training process
and adjusting hyperparameters in real-time. It provides a web interface to manage and interact
with the training process. It allows you to update model, optimizer, loss function, and other
hyperparameters in real-time.

Usage Example:

```python
from torchboard import board

class Classifier(nn.Module):
    def __init__(self, input_features=10, output_classes=5):
        super(Classifier, self).__init__()

        self.linear1 = torch.nn.Linear(input_features, 128)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(128, 64)
        self.activation2 = torch.nn.ReLU()
        self.linear3 = torch.nn.Linear(64, 32)
        self.activation3 = torch.nn.ReLU()
        self.linear4 = torch.nn.Linear(32, 16)
        self.activation4 = torch.nn.ReLU()
        self.linear5 = torch.nn.Linear(16, output_classes)
        self.softmax = torch.nn.Softmax()

    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        x = self.activation2(x)
        x = self.linear3(x)
        x = self.activation3(x)
        x = self.linear4(x)
        x = self.activation4(x)
        x = self.linear5(x)
        return self.softmax(x)


optimizer = optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999))
criterion = nn.CrossEntropyLoss()
acc = []
board.update(optimizer=optimizer, model=model, criterion=criterion)
model.train()
for epoch in range(epochs):
    optimizer.zero_grad()
    y_pred = model.forward(x_train)
    acc = (y_pred.argmax(dim=1) == y_train).float().mean()
    loss = criterion(y_pred, y_train)
    loss.backward()
    optimizer.step()
    sleep(0.1)
    board.update(acc=acc, acc2=acc - 0.2)
    validate(model, x_val, y_val, criterion)
sleep(10)
```

In this example, we have a simple classifier model, after getting access to optimizer, model and criterion
torchboard will allow you to access the web interface and change hyperparameters during the training as well
as to see automatically refreshed plots of what is happening.

- optimizer: enables modifying the hyperparameters used by optimizer in the training process
- model: gives access to the model (TODO: not fully supported yet)
- criterion: automatically updates the loss function used in the training process
- acc: adds new variable to the board to be displayed in the web interface
"""
from .base import Board

board = Board()

__all__ = ['board']
