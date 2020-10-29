import matplotlib.pyplot as plt

from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, iradon
from scipy.ndimage import zoom
import cv2 
image = cv2.imread('phantom.png', cv2.IMREAD_GRAYSCALE)
image = zoom(image, 0.4)

plt.figure(figsize=(8, 8.5))

#plt.subplot(221)
#plt.title("Original");
#plt.imshow(image, cmap=plt.cm.Greys_r)

plt.subplot(222)
projections = radon(image, theta=[45])
print(len(image))
print(len(projections))
plt.plot(projections);
plt.title("Projections at\n0, 45 and 90 degrees")
plt.xlabel("Projection axis");
plt.ylabel("Intensity");
plt.show()