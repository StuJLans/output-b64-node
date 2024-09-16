from server import PromptServer
from io import BytesIO
from PIL import Image
import numpy as np
import base64

class ImageOutput:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"default": None, "forceInput": True}),
                "Actions": ("STRING", {"default": ""})  # Set default to empty string
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    FUNCTION = "Proc"

    OUTPUT_NODE = True

    CATEGORY = "Knodes"  # You can change this category as needed
    
    def Proc(self, images, Actions=""):
        outs = []

        for single_image in images:
            # Convert image tensor to NumPy array and scale to [0, 255]
            img = np.asarray(single_image * 255., dtype=np.uint8)
            img = Image.fromarray(img)
            
            # Save image to a bytes buffer in PNG format
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            
            # Encode the image in base64
            img_str = base64.b64encode(buffered.getvalue()).decode()
            outs.append(img_str)

        # Send the base64-encoded images and actions via the PromptServer
        PromptServer.instance.send_sync("knodes", {"images": outs, "Actions": Actions})

        # Return the original images as output
        return (images,)
