import torch
import torch.nn as nn
import torch.optim as optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from torchboard import board

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


class DiabetesDataset(torch.utils.data.Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, ix):
        return self.X[ix], self.y[ix]

    def collate_fn(self, batch):
        X, y = zip(*batch)
        X = torch.stack(X)
        y = torch.tensor(y).float()
        return X, y


def train(model, train_loader, val_loader, epochs=100, lr=0.01):
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.7)
    criterion = nn.MSELoss()
    board.update(optimizer=optimizer, model=model, criterion=criterion)
    model.train()
    for epoch in range(epochs):
        for batch in train_loader:
            X, y = batch
            optimizer.zero_grad()
            y_pred = model.forward(X)
            loss = criterion(y_pred, y)
            loss.backward()
            optimizer.step()
            
            print(f"Epoch {epoch} loss: {loss.item()}")
        for batch in val_loader:
            X, y = batch
            validate(model, X, y, criterion)


@torch.no_grad()
def validate(model, x_val, y_val, criterion):
    model.eval()
    y_pred = model.forward(x_val)
    loss = criterion(y_pred, y_val)
    print(f"Validation loss: {loss.item()}")


if __name__ == "__main__":
    batch_size = 32
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)

    X_train, X_val, y_train, y_val = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )

    train_dataset = DiabetesDataset(X_train, y_train)
    valid_dataset = DiabetesDataset(X_val, y_val)

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=train_dataset.collate_fn,
        drop_last=True,
    )

    val_loader = torch.utils.data.DataLoader(
        valid_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=valid_dataset.collate_fn,
        drop_last=True,
    )

    model = Regressor(input_features=10)

    train(model, train_loader, val_loader, epochs=500, lr=0.0005)
