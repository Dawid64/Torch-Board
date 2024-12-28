import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from glob import glob
import torch
import torch.nn as nn
from torchvision import transforms as T
from torch.utils.data import Dataset, DataLoader
from torchvision import models

seed = 42
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'Currently using "{device}" device.')

batch_size = 6
image_size = 224
epochs = 10

path_images = r"cracks/images/"
path_masks = r"cracks/masks/"

images_paths = glob(path_images + "*.jpg")
masks_paths = glob(path_masks + "*.jpg")

images_paths = sorted(str(p) for p in images_paths)
masks_paths = sorted(str(p) for p in masks_paths)

df = pd.DataFrame({"images": images_paths, "masks": masks_paths})


train = df.sample(frac=1, random_state=seed)

print(f"Train size: {len(train)}")

train_transforms = T.Compose(
    [
        T.ToPILImage(),
        T.Resize((image_size, image_size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


class CrackDataset(Dataset):
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset.reset_index(drop=True)

        self.transforms = train_transforms

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, ix):
        row = self.dataset.loc[ix].squeeze()
        image_path = row["images"]
        mask_path = row["masks"]

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_tensor = self.transforms(image).float()
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = cv2.resize(mask, (image_size, image_size))

        label = 1 if np.any(mask) else 0

        return image_tensor, label

    def collate_fn(self, batch):
        images, labels = zip(*batch)
        images = torch.stack(images).to(device)
        labels = torch.tensor(labels).float().to(device)
        return images, labels


def get_mobile(output_channels=1):
    mobile = models.mobilenet_v3_large(weights=None)
    mobile.classifier = nn.Sequential(
        nn.Flatten(),
        nn.Linear(mobile.classifier[0].in_features, output_channels),
    )
    return mobile.to(device)


def train_one_batch(batch, model, criterion, optimizer):
    images, labels = batch
    optimizer.zero_grad()
    output = model(images).squeeze()
    predictions = (output >= 0.5).float()
    acc = (predictions == labels).float().mean()
    loss = criterion(output, labels)
    loss.backward()
    optimizer.step()
    return loss.item(), acc.item()


def train_epoch(
    model,
    criterion,
    optimizer,
    train_dataloader,
):
    epoch_train_losses = []
    epoch_train_accs = []

    model.train()
    for batch in train_dataloader:
        batch_train_loss, batch_train_acc = train_one_batch(
            batch, model, criterion, optimizer
        )
        epoch_train_losses.append(batch_train_loss)
        epoch_train_accs.append(batch_train_acc)
    epoch_train_loss = np.array(epoch_train_losses).mean()
    epoch_train_acc = np.array(epoch_train_accs).mean()

    print(f"Train loss: {epoch_train_loss:.4f}.")
    print(f"Train accuracy: {epoch_train_acc:.4f}.")


def full_suite(
    model,
    criterion,
    optimizer,
    epochs,
    lr,
    batch_size,
):
    train_dataset = CrackDataset(train)
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=train_dataset.collate_fn,
        drop_last=True,
    )

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    for i in range(1, epochs + 1):
        print(f"Epoch: {i}")
        train_epoch(
            model,
            criterion,
            optimizer,
            train_dataloader,
        )


full_suite(
    get_mobile(),
    nn.BCEWithLogitsLoss(),
    torch.optim.Adam,
    epochs,
    0.1,
    batch_size,
)
