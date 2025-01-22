import torch
import torch.nn as nn
import torch.optim as optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from time import sleep
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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


def train(model, x_train, y_train, x_val, y_val, epochs=100, lr=0.01):
    optimizer = optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999))
    criterion = nn.CrossEntropyLoss()
    # That is pretty much all you have to do to get the board running :)
    board.update(optimizer=optimizer, model=model, criterion=criterion)
    acc = []
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        y_pred = model.forward(x_train)
        acc = (y_pred.argmax(dim=1) == y_train).float().mean()
        loss = criterion(y_pred, y_train)
        loss.backward()
        optimizer.step()
        sleep(0.1)
        print(f"Epoch {epoch} loss: {loss.item()} accuracy: {acc}", end="\t")
        board.update(acc=acc, acc2=acc - 0.2)
        validate(model, x_val, y_val, criterion)
    sleep(2)


@torch.no_grad()
def validate(model, x_val, y_val, criterion):
    model.eval()
    y_pred = model.forward(x_val)
    loss = criterion(y_pred, y_val)
    print(f"Validation loss: {loss.item()}")


if __name__ == "__main__":
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    X_train, X_val, y_train, y_val = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )

    model = Classifier(input_features=4, output_classes=3)

    train(model, X_train, y_train, X_val, y_val, epochs=200, lr=0.01)
