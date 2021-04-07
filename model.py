import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3, padding=1)
        self.max1 = nn.MaxPool2d(kernel_size=2)
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(in_features=32*32*12, out_features=7)
    
    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.max1(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = self.fc1(x.reshape((x.shape[0],-1)))
        return x