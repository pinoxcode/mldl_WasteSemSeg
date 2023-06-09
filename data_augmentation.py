import os
from imgaug import augmenters as iaa
import cv2
import numpy as np


def augment_images(input_folder, output_folder, input_folder_l, output_folder_l, augmentation_factor):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    seq = iaa.Sequential([
        iaa.Fliplr(.5),
        iaa.Flipud(.5),
        iaa.Affine(rotate=(-90, 90)),
        iaa.Affine(scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}),
        iaa.Affine(translate_percent={"x": (-0.2, .2), "y": (-.2, .2)})
    ])

    x = 0
    num = 2750

    for filename in os.listdir(input_folder):
        if x % 100 == 0:
            print(x, "images augmented, ", num - x, "to go")
        if x == num:
            break
        x += 1
        if filename.endswith('.jpg') or filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.split('.')[0])
            input_path_l = os.path.join(input_folder_l, filename)
            output_path_l = os.path.join(output_folder_l, filename.split('.')[0])

            image = cv2.imread(input_path)
            label = cv2.imread(input_path_l)

            for i in range(augmentation_factor):
                seq_d = seq.to_deterministic()
                # IMAGES
                augmented_image = seq_d.augment_image(image)
                output_filename = f'{output_path}_augmented_{i}.jpg'
                cv2.imwrite(output_filename, augmented_image)

                # LABELS
                augmented_label = seq_d.augment_image(label)
                augmented_label = cv2.cvtColor(augmented_label, cv2.COLOR_BGR2GRAY)
                output_filename_l = f'{output_path_l}_augmented_{i}.jpg'
                cv2.imwrite(output_filename_l, augmented_label)

    print('Data augmentation completed.')


input_folder = '/content/drive/MyDrive/dataset/train'
output_folder = '/content/drive/MyDrive/dataset/train'
input_folder_l = '/content/drive/MyDrive/dataset/labels/train'
output_folder_l = '/content/drive/MyDrive/dataset/labels/train'
augmentation_factor = 1  # Generate augmentation_factor images for each input image

augment_images(input_folder, output_folder, input_folder_l, output_folder_l, augmentation_factor)
