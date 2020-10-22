import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageFrame:
    def __init__(self, image=None):
        self.image = image if image else np.zeros((512, 512, ), np.uint8)
        self.n_ovals = 0
        self.ovals = []

    def add_oval(self, oval):
        try:
            assert type(oval) == Oval
            self.ovals.append(oval)
        except TypeError:
            raise AssertionError('Input variable should be oval')

    def clear_ovals(self):
        self.ovals = []
        self.image = np.zeros((512, 512, ), np.uint8)

    def apply_ovals(self):
        frames = []
        how_to_norm = np.zeros_like(self.image)
        for oval in self.ovals:
            buffer_img = self.image.copy()
            img = cv2.ellipse(
                buffer_img.copy(),
                center=(oval.centroX, oval.centroY),
                axes=(oval.semiejeX, oval.semiejeY),
                angle=oval.inclinacion,
                startAngle=0,
                endAngle=360,
                color=self.__intensity2color(oval.intensidad),
                thickness=-1
                )
            intensity_img, htnorm = self.__color_to_intensity_normalized(img)
            how_to_norm += htnorm
            frames.append(intensity_img)

        float_img = self.image.copy().astype(np.float64)
        for img in frames:
            print(img.max())
            float_img += img

        print(how_to_norm.max())
        print(how_to_norm.min())
        print(float_img.max())
        print(float_img.min())

        for i in range(float_img.shape[0]):
            for j in range(float_img.shape[1]):
                if how_to_norm[i][j] >= 2:
                    float_img[i][j] = float_img[i][j] / how_to_norm[i][j]
                if float_img[i][j] > 1:
                    print("no")
                self.image[i][j] = int(np.interp(float_img[i][j], [-1, 1], [0, 255]))

        print(self.image.max())

    def __intensity2color(self, intensity):
        return int(np.interp(intensity, [-1, 1], [0, 255]))

    def __color_to_intensity_normalized(self, img):
        image = img.copy().astype(np.float64)
        ht_norm = np.zeros_like(img)
        # count = 0
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if img[i][j] != 0.0:
                    ht_norm[i][j] += 1
                    # count += 1
                image[i][j] = np.interp(image[i][j], [0, 255], [-1, 1])
        
        print(count)

        return image, ht_norm


class Oval:
    def __init__(self, intensidad, inclinacion, semiejeX, semiejeY, centroX, centroY):
        self.intensidad = intensidad
        self.inclinacion = inclinacion
        self.semiejeX = semiejeX
        self.semiejeY = semiejeY
        self.centroX = centroX
        self.centroY = centroY
