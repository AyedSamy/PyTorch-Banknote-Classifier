from torchvision import transforms
from PIL import Image

transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((64,64))])

def transform_image(image_path):
    """
    Check integrity of the image and transform it into a tensor if there is no issue
    """
    try:
        tensor = transform(Image.open(image_path))
        if tensor.shape[0] != 3:
            return "The provided image doesn't respect RGB format"
        else:
            return tensor
    except:
        return "The provided image is corrupted or doesn't exist"