import numpy as np
from scipy import misc
from os import listdir
from os.path import join
import cv2
from keras.models import load_model
import matplotlib.pyplot as plt
from utils import ycbcr2rgb
from test import psnr1,psnr


# 减少四周各6像素
def predict_nopadding():
    scale = 3
    input_size = 33
    label_size = 21
    padding_size = int((input_size - label_size) / 2)
    model_file = 'model-ep195-loss117.508-psnr31.481-20200525-14:38.h5'
    test_file = 'data/Test/Set5/baby_GT.bmp'

    model = load_model(model_file,custom_objects={'psnr1':psnr1})

    test_image = misc.imread(test_file, mode='YCbCr')
    w, h, c = test_image.shape
    # w -= w % scale
    # h -= h % scale
    w -= (w-input_size) % label_size
    h -= (h-input_size) % label_size
    test_image = test_image[0:w, 0:h, :]
    test_image[:, :, 1] = test_image[:, :, 0]
    test_image[:, :, 2] = test_image[:, :, 0]
    print(w,h)
    misc.imsave("sample/test_origin.bmp", test_image[padding_size: w-padding_size, padding_size: h-padding_size, :])

    scaled = misc.imresize(test_image, 1.0 / scale, 'bicubic')
    misc.imsave("sample/test_low.bmp",scaled)
    scaled = misc.imresize(scaled, scale / 1.0, 'bicubic')
    res_img = np.zeros(scaled.shape)
    psnrs=[]
    misc.imsave("sample/test_input.bmp", scaled[padding_size: w -padding_size, padding_size: h -padding_size, :])
    for i in range(0, w - input_size + 1, label_size):
        for j in range(0, h - input_size + 1, label_size):
            sub_img = scaled[i:i + input_size, j:j + input_size, :]
            prediction = model.predict(sub_img[None, :, :, 0, None])
            # print(prediction.shape)
            res_img[i + padding_size:i + padding_size + label_size,
            j + padding_size:j + padding_size + label_size,] = prediction
            psnrs.append(psnr(test_image[i + padding_size:i + padding_size + label_size,
            j + padding_size:j + padding_size + label_size,],prediction))
    res_img = res_img[padding_size:w -padding_size, padding_size:h-padding_size]
    misc.imsave("sample/test_res.bmp",res_img)
    print(np.mean(psnrs))


if __name__ == '__main__':
    predict_nopadding()
