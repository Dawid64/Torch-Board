import torch
import torch.nn as nn
import torch.optim as optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from torchboard import board
import time

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
        self.softmax = torch.nn.Softmax(1)

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
        x = self.softmax(x)
        return x


iris = datasets.load_iris()
X = iris.data
y = iris.target
def test_example():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target 


def test_example():
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    X_train, _, y_train, _ = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )

    model = Classifier(input_features=4, output_classes=3)

    optimizer = optim.Adam(model.parameters(), lr=.001)
    criterion = nn.CrossEntropyLoss()
    acc = []
    model.train()
    board.update(optimizer=optimizer, model=model, criterion=criterion)

    accuracies = []
    # Training loop
    for _ in range(100):
        optimizer.zero_grad()
        y_pred = model.forward(X_train)
        acc = (y_pred.argmax(dim=1) == y_train).float().mean()
        loss = criterion(y_pred, y_train)
        loss.backward()
        optimizer.step()

        board.update(acc=acc)
        accuracies.append(float(acc))
    assert board.model is model
    assert accuracies ==  board.history.history['acc']

def test_eval_train_saving():
    def train(model, x_train, y_train, x_val, y_val, epochs=2, lr=0.01):
        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        nn.HuberLoss
        acc = []
        board.update(optimizer=optimizer, model=model, criterion=criterion)
        print(board.criterion)
        for epoch in range(epochs):
            model.train()
            optimizer.zero_grad()
            y_pred = model.forward(x_train)
            acc = (y_pred.argmax(dim=1) == y_train).float().mean()
            loss = criterion(y_pred, y_train)
            loss.backward()
            optimizer.step()

            assert board.history.get_last() == {'criterion_train': loss.item()}

            validate(model, x_val, y_val, criterion)



    @torch.no_grad()
    def validate(model, x_val, y_val, criterion):
        model.eval()
        y_pred = model.forward(x_val)
        loss = criterion(y_pred, y_val)
        assert board.history.get_last() == {'criterion_eval': loss.item()}


    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    X_train, X_val, y_train, y_val = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )

    model = Classifier(input_features=4, output_classes=3)

    train(model, X_train, y_train, X_val, y_val, epochs=2, lr=0.01)





def test_eval_train_saving():
    def train(model, x_train, y_train, x_val, y_val, epochs=2, lr=0.01):
        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        nn.HuberLoss
        acc = []
        board.update(optimizer=optimizer, model=model, criterion=criterion)
        print(board.criterion)
        for epoch in range(epochs):
            model.train()
            optimizer.zero_grad()
            y_pred = model.forward(x_train)
            acc = (y_pred.argmax(dim=1) == y_train).float().mean()
            loss = criterion(y_pred, y_train)
            loss.backward()
            optimizer.step()

            assert board.history.get_last()['criterion_train'] == loss.item()

            validate(model, x_val, y_val, criterion)



    @torch.no_grad()
    def validate(model, x_val, y_val, criterion):
        model.eval()
        y_pred = model.forward(x_val)
        loss = criterion(y_pred, y_val)
        assert board.history.get_last()['criterion_eval'] == loss.item()


    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    X_train, X_val, y_train, y_val = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )

    model = Classifier(input_features=4, output_classes=3)

    train(model, X_train, y_train, X_val, y_val, epochs=50, lr=0.01)


if __name__ == '__main__': 
    test_example()