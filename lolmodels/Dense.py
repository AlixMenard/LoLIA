import os
import torch
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device}.")

class NeuralNetwork(nn.Module):
    def __init__(self, stack = None, lr = 0.001):
        super().__init__()
        self.X_train = self.y_train = None
        self.X_val = self.y_val = None
        self.flatten = nn.Flatten()
        if stack is None :
            self.stack = nn.Sequential(
                nn.Linear(273, 64),
                nn.ReLU(),
                nn.Dropout(p=0.3),
                nn.Linear(64, 16),
                nn.ReLU(),
                nn.Dropout(p=0.3),
                nn.Linear(16, 1),
            )
        else :
            self.stack = stack
        self.loss_fn = nn.BCELoss()  # binary cross entropy
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.to(device)

    def forward(self, x):
        x = self.flatten(x)
        logits = self.stack(x)
        logits = torch.sigmoid(logits)
        return logits

    def fit(self, X=None, y=None, n_epochs = 100, batch_size = 64, verbose = False):
        if X is None:
            if self.X_train is None:
                return
            X = self.X_train
        if y is None:
            if self.y_train is None:
                return
            y = self.y_train
        self.train()

        for epoch in range(n_epochs):
            for i in range(0, len(X), batch_size):
                Xbatch = X[i:i + batch_size]
                y_pred = self(Xbatch)
                ybatch = y[i:i + batch_size]
                loss = self.loss_fn(y_pred, ybatch)

                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()
            if verbose:
                print(f'Epoch {epoch+1}/{n_epochs}, latest loss {loss}')

    def test(self):
        self.eval()

        with torch.no_grad():
            pred = self(self.X_val)
            test_loss = self.loss_fn(pred, self.y_val).item()
            predicted = (pred >= 0.5).float()
            correct = (predicted == self.y_val).sum().item()
            accuracy = 100 * correct / len(self.y_val)
            print(f"Test Error: \n Accuracy: {(accuracy):>0.1f}%, Avg loss: {test_loss:>8f} \n")
        return accuracy, test_loss

    def format(self, train, val):
        X_train, y_train = train[:,1:], train[:,0]
        X_val, y_val = val[:, 1:], val[:, 0]

        self.X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
        self.y_train = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1).to(device)
        self.X_val = torch.tensor(X_val, dtype=torch.float32).to(device)
        self.y_val = torch.tensor(y_val, dtype=torch.float32).reshape(-1, 1).to(device)

        assert len(self.X_train) == len(self.y_train), f"Train samples and labels have different lengths ({self.X_train.shape} and {self.y_train.shape})"
        assert len(self.X_val) == len(self.y_val), f"Validation samples and labels have different lengths ({self.X_val.shape} and {self.y_val.shape})"
        first_parameter = next(self.parameters())
        input_shape = first_parameter.size()
        assert len(self.X_train[0]) == input_shape[-1], f"Samples and model input have different sizes ({len(self.X_train[0])} and {input_shape[-1]})"
