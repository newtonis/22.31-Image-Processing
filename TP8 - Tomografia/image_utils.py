import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageFrame:
    def __init__(self, image=None):
        self.image = image if image else np.zeros((512, 512, 3), np.uint8)
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
        self.image = np.zeros((512, 512, 3), np.uint8)

    def apply_ovals(self):
        for oval in self.ovals:
            cv2.ellipse(
                self.image,
                center=(oval.centroX, oval.centroY),
                axes=(oval.semiejeX, oval.semiejeY),
                angle=oval.inclinacion,
                startAngle=0,
                endAngle=360,
                color=self.__intensity2color(oval.intensidad),
                thickness=-1
                )

    def __intensity2color(self, intensity):
        return (255, 0, 0) 


class Oval:
    def __init__(self, intensidad, inclinacion, semiejeX, semiejeY, centroX, centroY):
        self.intensidad = intensidad
        self.inclinacion = inclinacion
        self.semiejeX = semiejeX
        self.semiejeY = semiejeY
        self.centroX = centroX
        self.centroY = centroY
