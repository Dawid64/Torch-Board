import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms as T
from torch.utils.data import DataLoader
from torchvision import models, datasets

seed = 42
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'Currently using "{device}" device.')

batch_size = 64
image_size = 224
epochs = 30


def get_mobile(output_channels=1):
    mobile = models.mobilenet_v3_large(weights=None)
    mobile.classifier = nn.Sequential(
        nn.Flatten(),
        nn.Linear(mobile.classifier[0].in_features, output_channels),
        nn.Softmax(dim=1),
    )
    return mobile.to(device)


def train_one_batch(images, labels, model, criterion, optimizer):
    images = images.to(device)
    labels = labels.to(device)
    optimizer.zero_grad()
    output = model(images).squeeze()
    predicted_class = torch.argmax(output, dim=1)
    acc = (predicted_class == labels).float().mean()
    loss = criterion(output, labels)
    loss.backward()
    optimizer.step()
    return loss.item(), acc


def train_epoch(
    model,
    criterion,
    optimizer,
    train_dataloader,
):
    epoch_train_losses = []
    epoch_train_accs = []

    model.train()
    for x, y in train_dataloader:
        batch_train_loss, acc = train_one_batch(x, y, model, criterion, optimizer)
        epoch_train_losses.append(batch_train_loss)
        epoch_train_accs.append(acc.cpu())
    epoch_train_loss = np.array(epoch_train_losses).mean()
    epoch_train_acc = np.array(epoch_train_accs).mean()

    print(f"Train loss: {epoch_train_loss:.4f}.")
    print(f"Train accuracy: {epoch_train_acc:.4f}.")


def full_suite(model, epochs, lr, batch_size):
    train_transforms = T.Compose(
        [
            T.Grayscale(num_output_channels=3),
            T.Resize((image_size, image_size)),
            T.ToTensor(),
        ]
    )

    train_dataset = datasets.FashionMNIST(
        root="data", train=True, download=True, transform=train_transforms
    )

    num_samples = 600
    indices = np.random.choice(len(train_dataset), size=num_samples, replace=False)
    train_dataset = torch.utils.data.Subset(train_dataset, indices)
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, drop_last=True
    )

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adagrad(model.parameters(), lr=lr, lr_decay=0.0001)
    for i in range(1, epochs + 1):
        print(f"Epoch: {i}")
        train_epoch(model, criterion, optimizer, train_loader)


full_suite(
    get_mobile(output_channels=10),
    epochs,
    0.1,
    batch_size,
)
