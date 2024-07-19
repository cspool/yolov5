import torch
import cv2
from torchinfo import summary


# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

# Images
img = "./game_box/street.JPG"  # or file, Path, PIL, OpenCV, numpy, list

# Images
# img = "https://ultralytics.com/images/zidane.jpg"  # or file, Path, PIL, OpenCV, numpy, list
# im0 = cv2.imread(img)  # BGR
# t_im0 = torch.from_numpy(im0)
# t_im1 = t_im0.permute(2,1,0)
# t_im2 = t_im1[:,0:1024,0:1024]

batch_size = 16
summary(model, input_size=(batch_size, 3, 1024, 1024), verbose=1, depth=8 ,
        col_names=["input_size",
                "output_size",
                "num_params",
                "kernel_size",])

# Inference
# results = model(img)

# Results
# results.print()  # or .show(), .save(), .crop(), .pandas(), etc.