import os; os.environ['DISPLAY'] = ':0' # Para correr en linux
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Me base en esta implementación: https://www.giassa.net/?page_id=371

img = cv2.imread("mono.bmp", cv2.IMREAD_GRAYSCALE)

def resize_bicubic_interpol(img, scale):
    new_img = np.zeros((img.shape[0]*scale, img.shape[1]*scale), dtype=np.uint8)
    new_img[::scale, ::scale] = img[::]
    M_inv = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-3, 3, 0, 0, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, -2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, 0, -2, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1, 1, 0, 0],
        [-3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1 ,0],
        [9, -9, -9, 9, 6, 3, -6, -3, 6, -6, 3, -3, 4, 2, 2, 1],
        [-6, 6, 6, -6, -3, -3, 3, 3, -4, 4, -2, 2, -2, -2, -1, -1],
        [2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [-6, 6, 6, -6, -4, -2, 4, 2, -3, 3, -3, 3, -2, -1, -2, -1],
        [4, -4, -4, 4, 2, 2, -2, -2, 2, -2, 2, -2, 1, 1, 1, 1]
    ])

    def fx(img, X, Y):
        try:
            return (img[X + 1, Y] - img[X - 1, Y]) / 2
        except IndexError:
            print(f'Index error at: {X}, {Y}')
            return 0

    def fy(img, X, Y):
        try:
            return (img[X, Y + 1] - img[X, Y - 1]) / 2
        except IndexError:
            print(f'Index error at: {X}, {Y}')
            return 0

    def fxy(img, X, Y):
        try:
            return (img[X - 1, Y - 1] + img[X + 1, Y + 1] - img[X + 1, Y - 1] - img[X - 1, Y + 1]) / 4
        except IndexError:
            print(f'Index error at: {X}, {Y}')
            return 0

    def compute(X, Y, A, B, X2, Y2, alpha):
        value = 0
        for i in range(4):
            for j in range(4):
                value += alpha[i*4 + j] * (((X - A) / (X2 - A))**i) * (((Y - B) / (Y2 - B)) **j)
                # print((((X - A) / (X2 - A))**i) * (((Y - B) / (Y2 - B)) **j))
                # print(alpha[i*4 + j])
        return abs(value)

    alpha_vectors = {}
    for i in range(len(img)):
        for j in range(len(img)):
            try:
#                beta = np.array([
#                   img[i, j], img[i + 1, j], img[i, j + 1], img[i + 1, j + 1],
#                    fx(img, i, j), fx(img, i + 1, j), fx(img, i, j + 1), fx(img, i + 1, j + 1),
#                    fy(img, i, j), fy(img, i + 1, j), fy(img, i, j + 1), fy(img, i + 1, j + 1),
#                    fxy(img, i, j), fxy(img, i + 1, j), fxy(img, i, j + 1), fxy(img, i + 1, j + 1)
#                    ])
                beta = np.array([
                   img[i, j], img[i + 1, j], img[i, j + 1], img[i + 1, j + 1],
                    cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)[i, j], cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)[i+1, j], cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)[i, j + 1], cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)[i+1, j+1],
                    cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)[i, j], cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)[i+1, j], cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)[i, j + 1], cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)[i+1, j+1],
                    cv2.Sobel(cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3),cv2.CV_64F,0,1,ksize=3)[i, j], cv2.Sobel(cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3),cv2.CV_64F,0,1,ksize=3)[i+1, j], cv2.Sobel(cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3),cv2.CV_64F,0,1,ksize=3)[i, j+1], cv2.Sobel(cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3),cv2.CV_64F,0,1,ksize=3)[i+1, j+1]
                    ])
                alpha = np.dot(M_inv, np.transpose(beta))
                # alpha = alpha.reshape((4, 4))
                alpha_vectors[(i, j)] = alpha
            except IndexError:
                print(f'Error at index {i}, {j}')

    for x in range(new_img.shape[0]):
        for y in range(new_img.shape[1]):
            y1 = y // scale
            x1 = x // scale
            y2 = ((y1+1)*scale)
            x2 = ((x1+1)*scale)
            try:
                if(alpha_vectors[(x1, y1)].any()):
                    new_img[x, y] = compute(x, y, x1, y1, x2, y2, alpha_vectors[(x1, y1)])
            except (IndexError, KeyError):
                print(f'Failed at {x}, {y}')

    return new_img

plt.imshow(
    np.hstack(
        [resize_bicubic_interpol(img[0::4, 0::4], 4),
        cv2.resize(img[0::4, 0::4], (256, 256), cv2.INTER_CUBIC)]
        ),
    cmap="gray", vmin=0, vmax=255
    )
plt.show()
plt.imshow(resize_bicubic_interpol(img[0::4, 0::4], 4), cmap="gray", vmin=0, vmax=255)
plt.show()
plt.imshow(img[0::4, 0::4], cmap="gray", vmin=0, vmax=255)
plt.show()
