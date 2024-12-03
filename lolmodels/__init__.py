__all__ = ['Dense', 'GBC', 'KNN', 'random_forest', 'RNN', 'SGD', 'NGD', "format"]

import torch
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using device: {device}")

def format(batch):
    if len(batch.shape) == 2:
        X, y = batch[:, 1:], batch[:, 0]

        X = torch.tensor(X, dtype=torch.float32).to(device)
        y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1).to(device)

        return X, y
    else:
        X, y = batch[:,:,1:], batch[:,0,0]

        X = torch.tensor(X, dtype=torch.float32).to(device)
        y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1).to(device)

        return X, y
