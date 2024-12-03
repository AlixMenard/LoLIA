__all__ = ['Dense', 'GBC', 'KNN', 'random_forest', 'RNN', 'SGD', 'NGD']

import torch
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

def format(*args):
    ret = []
    for batch in args:
        X, y = train[:, 1:], train[:, 0]

        X = torch.tensor(X, dtype=torch.float32).to(device)
        y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1).to(device)