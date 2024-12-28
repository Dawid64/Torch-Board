import torch
import torch.nn as nn
import torch.optim as optim
from sklearn import datasets
from sklearn.model_selection import train_test_split


class Regressor(nn.Module):
    def __init__(self, input_features=10):
        super(Regressor, self).__init__()

        self.linear1 = torch.nn.Linear(input_features, 128)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(128, 64)
        self.activation2 = torch.nn.ReLU()
        self.linear3 = torch.nn.Linear(64, 32)
        self.activation3 = torch.nn.ReLU()
        self.linear4 = torch.nn.Linear(32, 16)
        self.activation4 = torch.nn.ReLU()
        self.linear5 = torch.nn.Linear(16, 1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        x = self.activation2(x)
        x = self.linear3(x)
        x = self.activation3(x)
        x = self.linear4(x)
        x = self.activation4(x)
        return self.linear5(x)


def train(model, x_train, y_train, x_val, y_val, epochs=100, lr=0.01):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        y_pred = model.forward(x_train)
        loss = criterion(y_pred, y_train)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch} loss: {loss.item()}")
        validate(model, x_val, y_val, criterion)


@torch.no_grad()
def validate(model, x_val, y_val, criterion):
    model.eval()
    y_pred = model.forward(x_val)
    loss = criterion(y_pred, y_val)
    print(f"Validation loss: {loss.item()}")


if __name__ == "__main__":
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)

    X_train, X_val, y_train, y_val = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )

    model = Regressor(input_features=10)

    train(model, X_train, y_train, X_val, y_val, epochs=50, lr=0.01)
