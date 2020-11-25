import cv2
from PIL import Image

# Returns if the ending of the sent file is, in fact, an image
# This prevents people from sending a non-image file
def pic_ending(string):
    return string.endswith(".jpg") or string.endswith(".jpeg") or string.endswith(".png"):

def convertImage(path, imageName):
    im = Image.open(path+imageName).convert("RGB")
    im.save("getpfpImages/"+imageName+".png", "png")
    return "getpfpImages/"+imageName+".png"