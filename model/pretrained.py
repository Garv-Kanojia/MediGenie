import torch
from torchvision import models
import torch.nn as nn

model = models.densenet161(weights=None)

#Change Architecture
model.features.conv0 = nn.Conv2d(1, 96, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
num_ftrs = model.classifier.in_features
model.classifier = nn.Linear(num_ftrs, 14)

#Load Weights
model.load_state_dict(torch.load("model_weights_main.pt" , weights_only=True , map_location=torch.device('cpu')))