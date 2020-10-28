import os; os.environ['DISPLAY'] = ':0' # LINEA DE CODIGO MAGICA:
import tkinter as tk
import matplotlib.pyplot as plt
from image_utils import ImageFrame, Oval
import cv2

class Application(tk.Frame):
    """ https://wiki.python.org/moin/TkInter """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

print(__name__)

if __name__ == "__main__":
    print(__name__)
    # root = tk.Tk()
    # app = Application(master=root)
    # app.mainloop()
    image_frame = ImageFrame()
    oval1 = Oval(
        intensidad=1,
        inclinacion=45,
        semiejeX=60,
        semiejeY=100,
        centroX=350,
        centroY=300
    )

    oval2 = Oval(
        intensidad=-0.999,
        inclinacion=90,
        semiejeX=50,
        semiejeY=100,
        centroX=300,
        centroY=200
    )

    oval3 = Oval(
        intensidad=-0.4,
        inclinacion=90,
        semiejeX=50,
        semiejeY=100,
        centroX=500,
        centroY=450
    )

    image_frame.add_oval(oval1)
    image_frame.add_oval(oval2)
    image_frame.add_oval(oval3)
    image_frame.apply_ovals()

    fig = plt.figure(figsize=(14, 10))
    fig.add_subplot(1, 2, 1)
    plt.title('img')
    plt.imshow(image_frame.image, cmap='gray', vmin=0, vmax=255)
    plt.show()

    # image_frame.clear_ovals()

    # plt.imshow(image_frame.image)