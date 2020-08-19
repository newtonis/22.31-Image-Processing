#https://stackoverflow.com/questions/52700878/bicubic-interpolation-python

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import cv2

img_original = cv2.imread("mono.bmp", cv2.IMREAD_GRAYSCALE)
img = img_original[::4,::4]

def bicubic_interpolation2(xi, yi, zi, xnew, ynew):

    z = np.zeros((xnew.size, ynew.size))

    for n, x in enumerate(xnew):
        for m, y in enumerate(ynew):
            try:
            # if xi.min() <= x <= xi.max() and yi.min() <= y <= yi.max():
                i = np.searchsorted(xi, x) - 1  
                j = np.searchsorted(yi, y) - 1

                x1  = xi[i]
                x2  = xi[i+1]

                y1  = yi[j]
                y2  = yi[j+1]

                px = (x-x1)/(x2-x1)
                py = (y-y1)/(y2-y1)

                f00 = zi[i-1, j-1]      #row0 col0 >> x0,y0
                f01 = zi[i-1, j]        #row0 col1 >> x1,y0
                f02 = zi[i-1, j+1]      #row0 col2 >> x2,y0

                f10 = zi[i, j-1]        #row1 col0 >> x0,y1
                f11 = p00 = zi[i, j]    #row1 col1 >> x1,y1
                f12 = p01 = zi[i, j+1]  #row1 col2 >> x2,y1

                f20 = zi[i+1,j-1]       #row2 col0 >> x0,y2
                f21 = p10 = zi[i+1,j]   #row2 col1 >> x1,y2
                f22 = p11 = zi[i+1,j+1] #row2 col2 >> x2,y2

                if 0 < i < xi.size-2 and 0 < j < yi.size-2:

                    f03 = zi[i-1, j+2]      #row0 col3 >> x3,y0

                    f13 = zi[i,j+2]         #row1 col3 >> x3,y1

                    f23 = zi[i+1,j+2]       #row2 col3 >> x3,y2

                    f30 = zi[i+2,j-1]       #row3 col0 >> x0,y3
                    f31 = zi[i+2,j]         #row3 col1 >> x1,y3
                    f32 = zi[i+2,j+1]       #row3 col2 >> x2,y3
                    f33 = zi[i+2,j+2]       #row3 col3 >> x3,y3

                elif i<=0: 

                    f03 = f02               #row0 col3 >> x3,y0

                    f13 = f12               #row1 col3 >> x3,y1

                    f23 = f22               #row2 col3 >> x3,y2

                    f30 = zi[i+2,j-1]       #row3 col0 >> x0,y3
                    f31 = zi[i+2,j]         #row3 col1 >> x1,y3
                    f32 = zi[i+2,j+1]       #row3 col2 >> x2,y3
                    f33 = f32               #row3 col3 >> x3,y3             

                elif j<=0:

                    f03 = zi[i-1, j+2]      #row0 col3 >> x3,y0

                    f13 = zi[i,j+2]         #row1 col3 >> x3,y1

                    f23 = zi[i+1,j+2]       #row2 col3 >> x3,y2

                    f30 = f20               #row3 col0 >> x0,y3
                    f31 = f21               #row3 col1 >> x1,y3
                    f32 = f22               #row3 col2 >> x2,y3
                    f33 = f23               #row3 col3 >> x3,y3


                elif i == xi.size-2 or j == yi.size-2:

                    f03 = f02               #row0 col3 >> x3,y0

                    f13 = f12               #row1 col3 >> x3,y1

                    f23 = f22               #row2 col3 >> x3,y2

                    f30 = f20               #row3 col0 >> x0,y3
                    f31 = f21               #row3 col1 >> x1,y3
                    f32 = f22               #row3 col2 >> x2,y3
                    f33 = f23               #row3 col3 >> x3,y3

                Z = np.array([f00, f01, f02, f03,
                             f10, f11, f12, f13,
                             f20, f21, f22, f23,
                             f30, f31, f32, f33]).reshape(4,4).transpose()

                X = np.tile(np.array([-1, 0, 1, 2]), (4,1))
                X[0,:] = X[0,:]**3
                X[1,:] = X[1,:]**2
                X[-1,:] = 1

                Cr = Z@np.linalg.inv(X)
                R = Cr@np.array([px**3, px**2, px, 1])

                Y = np.tile(np.array([-1, 0, 1, 2]), (4,1)).transpose()
                Y[:,0] = Y[:,0]**3
                Y[:,1] = Y[:,1]**2
                Y[:,-1] = 1

                Cc = np.linalg.inv(Y)@R

                z[n,m]=(Cc@np.array([py**3, py**2, py, 1]))
            except:
                print("failed at:",n,m)
                pass
    return z

x = np.array(range(len(img)))#np.linspace(-6, 6, 11)
y = np.array(range(len(img)))#np.linspace(-6, 6, 11)

scale = 2

x_new = np.array(range(scale*len(img)))/scale#np.linspace(-6, 6, 11)
y_new = np.array(range(scale*len(img)))/scale#np.linspace(-6, 6, 11)

z_new = bicubic_interpolation2(x, y, img, x_new, y_new)

plt.imshow(z_new, cmap='gray', vmin=0, vmax=255)
plt.show()