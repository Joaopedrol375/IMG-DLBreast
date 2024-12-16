# -*- coding: utf-8 -*-
"""dataImport.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gb9Hj-FQWbZsjtCbnZC1d9BRrfpznIN7
"""

import pandas as pd
import os
import numpy as np
import torch
import matplotlib.image as mpimg
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import cv2
from skimage import io, color
from skimage import color as skcolor
from torchvision import transforms
import torchvision.transforms as T
from PIL import Image
import torchvision.transforms.functional as F

class DBTData(Dataset):
    def __init__(self, filepath, mode, crop_to=(224,224), resize_to=(256, 256), color=True):
        self._crop_to = crop_to
        self._resize_to = resize_to
        self._color = color
        self.mode = mode
        self.filepath = filepath

        # ATTENTION: only adjust the file path here !#
        # load csv file and image according to mode
        if mode == "train":
            df = pd.read_csv("/content/drive/MyDrive/1209full_data/label/train.csv")
            filepath = "/content/drive/MyDrive/1209full_data/train"
        elif mode == "valid":
            df = pd.read_csv("/content/drive/MyDrive/1209full_data/label/validation.csv")
            filepath = "/content/drive/MyDrive/1209full_data/validation"
        elif mode == "test":
            df = pd.read_csv("/content/drive/MyDrive/1209full_data/label/validation.csv")
            filepath = "/content/drive/MyDrive/1209full_data/validation"

        # extract label
        y = df["type"].values
        self.len = len(y)
        x = []

        # load images
        for i in range(self.len):
            Slice = df.at[i, "filename"]  # 'filename'
            image_path = os.path.join(filepath, Slice)

            try:
                img = mpimg.imread(image_path)
                if len(img.shape) == 3:  #  RGB image，transform to grey image
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                x.append(img)
            except FileNotFoundError:
                print(f"File {image_path} not found")
                continue

        self.x = x
        self.y = torch.from_numpy(y)

#     def divide_by_255(self, x):
#         return x / 255.0

    def __getitem__(self, idx):
        x = self.x[idx]
        if self._color:
            x = skcolor.gray2rgb(x)  #  RGB image
        y = self.y[idx]
        # CrossEntropyLoss does not expect a one-hot encoded vector, but class indices

        def custom_preprocessing(image):
          # Apply noise to the image
          noisy_image = add_noise_to_image(image)
          
          # Apply blur to the image
          blurred_image = apply_blur_to_image(noisy_image)
          
          # Adjust contrast and brightness
          enhanced_image = adjust_contrast_brightness(blurred_image)

          return enhanced_image

        def add_noise_to_image(image):
            # Add noise to the image (customize this function as needed)
            noisy_image = np.clip(image + np.random.normal(loc=0, scale=0.1, size=image.shape), 0, 1)
            return noisy_image

        def apply_blur_to_image(image):
            # Apply blur to the image (customize this function as needed)
            blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
            return blurred_image

        def adjust_contrast_brightness(image_tensor):
            # Convert PyTorch tensor to PIL image for transformations
            pil_img = F.to_pil_image(image_tensor)
            
            # Adjust contrast (factor=1.5)
            pil_img = F.adjust_contrast(pil_img, contrast_factor=1.5)
            
            # Adjust brightness (factor=1.2)
            pil_img = F.adjust_brightness(pil_img, brightness_factor=1.2)
            
            # Convert PIL image back to PyTorch tensor
            enhanced_img_tensor = F.to_tensor(pil_img)
            
            return enhanced_img_tensor
          

        x = np.atleast_3d(x)  # I love numpy!
        x = x.astype(np.uint8)
        x = Image.fromarray(x.astype(np.uint8))
#         trans = transforms.Compose([
#             transforms.ToPILImage(),
# #             transforms.CenterCrop(self._crop_to),
            
#             transforms.Resize(self._resize_to),
#             transforms.ToTensor(),
# #             transforms.Grayscale(num_output_channels=1),
# #             transforms.Normalize(mean=[0.5], std=[0.5])
# #             transforms.Normalize(mean=[0], std=[1/255])
# #             self.divide_by_255
# #             // %255
#         ])
#         x = trans(x)
        # mean_nums = [.275, .275, .275]
        # std_nums = [.197, .197, .197]

        # train_transforms = T.Compose([
        #   T.Resize([299,299]),
        #   T.RandomRotation(degrees=5),
        #   T.RandomHorizontalFlip(),
        #   T.RandomPerspective(),
        #   T.ToTensor(),
        #   T.Normalize(mean_nums, std_nums)])

        # valid_transforms = T.Compose([
        #   T.Resize([299,299]),
        #   T.RandomRotation(degrees=5),
        #   T.RandomHorizontalFlip(),
        #   T.RandomPerspective(),
        #   T.ToTensor(),
        #   T.Normalize(mean_nums, std_nums)
        # ])

        # test_transforms = T.Compose([
        #   T.Resize([299,299]),
        #   T.ToTensor(),
        #   T.Normalize(mean_nums, std_nums)
        # ])

        
        augmentation_class1 = T.Compose([
          T.RandomRotation(degrees=5), 
          T.RandomHorizontalFlip(p=0.5),
          # transforms.RandomResizedCrop(size=(height, width), scale=(0.9, 1.1)), 
          T.RandomAffine(degrees=5, translate=(0.1, 0.1))  
          # T.ToTensor()  
        ])

        datagen = T.Compose([
          T.RandomHorizontalFlip(p=1.0),  # Always apply horizontal flip
          T.RandomVerticalFlip(p=1.0),    # Always apply vertical flip
          T.Pad(padding=10, padding_mode='edge') # Fill missing pixels with the nearest value
          # T.ToTensor()
        ])

        test_trans = T.Compose([
          T.Resize([299,299]),
          T.ToTensor()
        ])

        
        if self.mode == "train":
          # x = x.view(-1, 224, 224, 3)
          x = test_trans(x)
          x = datagen(x)
          if y == 1:  # Check for class 1
            x = augmentation_class1(x)
        elif self.mode == "valid":
          x = test_trans(x)


        return x, y

    def __len__(self):  # return datalength
        return self.len

# dataset = DBTData('train_phase2')
# train_loader = DataLoader(dataset=dataset, batch_size=32, shuffle=True, num_workers=2)