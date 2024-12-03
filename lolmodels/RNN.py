import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from . import device

class SimpleRNN(nn.Module):

    name = "RNN"

    # ! hidden_size = 4, num_layers = 1, lr = 1e-5
    # ? Accuracy : 67.47%, MSE : 0.379
    def __init__(self, input_size = 273, hidden_size = 1, output_size = 1, num_layers = 1, lr = 1e-5):
        # input_size: Number of features in the input data.
        # hidden_size: Number of units in the RNN’s hidden layer.
        # output_size: Number of classes (for binary classification, set to 1 or 2).
        # num_layers: Number of RNN layers.
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # RNN Layer
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)

        # Output layer
        self.fc = nn.Linear(hidden_size, output_size)

        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.parameters(), lr = lr)

        self.X_train = self.y_train = None
        self.X_test = self.y_test = None

        self.to(device)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Forward propagate through RNN
        out, _ = self.rnn(x, h0)

        # Use the last time-step's output for classification
        out = self.fc(out[:, -1, :])
        return out

    def fit(self, X=None, y=None, n_epochs = 200, batch_size = 64, verbose = False):
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
                ybatch = y[i:i + batch_size]

                # Forward pass
                outputs = self(Xbatch)
                loss = self.criterion(outputs, ybatch)

                # Backward pass and optimization
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            if (epoch + 1) % 10 == 0 and verbose:
                print(f'Epoch [{epoch + 1}/{n_epochs}], Loss: {loss.item():.4f}')

    def test(self, X=None, y=None):
        if X is None:
            if self.X_val is None:
                return
            X = self.X_val
        if y is None:
            if self.y_val is None:
                return
            y = self.y_val
        self.eval()

        with torch.no_grad():
            pred = self(X)
            test_loss = self.criterion(pred, y).item()
            predicted = (pred >= 0.5).float()
            mse = ((pred - y)**2).mean().item()
            correct = (predicted == y).sum().item()
            accuracy = 100 * correct / len(y)
            print(f"Test Error: Accuracy: {(accuracy):>0.1f}%, MSE : {mse:>8f}")
        return accuracy, mse

    def format(self, train, val):
        X_train, y_train = train[:,:,1:], train[:,0,0]
        X_val, y_val = val[:,:,1:], val[:,0,0]

        self.X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
        self.y_train = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1).to(device)
        self.X_val = torch.tensor(X_val, dtype=torch.float32).to(device)
        self.y_val = torch.tensor(y_val, dtype=torch.float32).reshape(-1, 1).to(device)

        assert len(self.X_train) == len(self.y_train), f"Train samples and labels have different lengths ({self.X_train.shape} and {self.y_train.shape})"
        assert len(self.X_val) == len(self.y_val), f"Validation samples and labels have different lengths ({self.X_val.shape} and {self.y_val.shape})"
        first_parameter = next(self.parameters())
        input_shape = first_parameter.size()
        assert len(self.X_train[0][0]) == input_shape[-1], f"Samples and model input have different sizes ({len(self.X_train[0][0])} and {input_shape[-1]})"