from model import NeuralNet
import torch

def get_prediction(x):
    """
    get prediction from transformed image tensor x
    """
    my_model = NeuralNet()
    with open("best_model.pth", "rb") as f:
        best_state_dict = torch.load(f)
    my_model.load_state_dict(best_state_dict)
    z = my_model(x.reshape((1,3,64,64)))
    z = torch.softmax(z, 1) # Apply a softmax function to the array to get the corresponding probability of each class
    _, yhat = torch.max(z, 1) # Check the argmax (column index of the maximum value in the z array) to get the predicted label yhat
    return yhat[0].item(), z[0].detach()