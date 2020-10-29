from gui_radon import *
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import matplotlib.pyplot as plt

from image_utils import ImageFrame, Oval, cv2, iradon, np, plt, radon
import random

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

def elipseToOvals(Intensidad,SemiEjeX,SemiEjeY,CentroX,CentroY,Inclinacion):
    return Oval(Intensidad, Inclinacion, SemiEjeX, SemiEjeY, CentroX, CentroY)

class elipse():    
    def __init__(self,Intensidad = None,SemiEjeX=None,SemiEjeY=None,CentroX=None,CentroY=None,Inclinacion=None):
        self.Intensidad = Intensidad  
        self.SemiEjeX = SemiEjeX      
        self.SemiEjeY = SemiEjeY      
        self.CentroX = CentroX        
        self.CentroY = CentroY        
        self.Inclinacion = Inclinacion

    def str_with_params(self):
        return (f"Int:{self.Intensidad},SemiEjeX:{self.SemiEjeX},SemiEjeY:{self.SemiEjeY},CX:{self.CentroX},CY:{self.CentroY},Inclin:{self.Inclinacion}")


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        self.elipse_list = []
        self.displayed_elipse = elipse()
        self.image_frame = ImageFrame()


        self.canvas = MplCanvas(self, width=3, height=3, dpi=100)
        self.canvas.move(400,50)


        #asignamos la funcion asociada al evento textChanged
        self.lineEditIntensidad.textChanged.connect(self.textChangedIntensidad) # double
        self.lineEditIntensidad.setValidator(QtGui.QDoubleValidator(1.0,-1.0,4,notation=QtGui.QDoubleValidator.StandardNotation))
        
        self.lineEditSemiEjeX.textChanged.connect(self.textChangedSemiEjeX)
        self.lineEditSemiEjeX.setValidator(QtGui.QIntValidator(-1000,1000))
        
        self.lineEditSemiEjeY.textChanged.connect(self.textChangedSemiEjeY)
        self.lineEditSemiEjeY.setValidator(QtGui.QIntValidator(-1000,1000))

        
        self.lineEditCentroX.textChanged.connect(self.textChangedCentroX)
        self.lineEditCentroX.setValidator(QtGui.QIntValidator(-1000,1000))

        
        self.lineEditCentroY.textChanged.connect(self.textChangedCentroY)
        self.lineEditCentroY.setValidator(QtGui.QIntValidator(-1000,1000))


        self.lineEditInclinacion.textChanged.connect(self.textChangedInclinacion) # double
        self.lineEditInclinacion.setValidator(QtGui.QDoubleValidator(1.0,-1.0,4,notation=QtGui.QDoubleValidator.StandardNotation))

        #asignamos la funcion asociada al evento clicked en push buttons
        self.pushButtonAgregar.clicked.connect(self.onClickAgregar)
        self.pushButtonBorrar.clicked.connect(self.onClickBorrar)
    
    def update_plot(self,image):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.imshow(image)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def areAllParamsDisplayedValid(self):
        if(self.validateNumberIntensidad() and self.validateNumberSemiEjeX() and self.validateNumberSemiEjeY()
        and self.validateNumberCentroX() and self.validateNumberCentroY() and self.validateNumberInclinacion()):
            return True
        else:
            return False
            
        #escribimos la funcion asociada al evento clicked en push buttons

    def updateElipseGraphics(self):
        for e in self.elipse_list:
           currOval = elipseToOvals(e.Intensidad,e.SemiEjeX,e.SemiEjeY,e.CentroX,e.CentroY,e.Inclinacion)
           self.image_frame.add_oval(currOval)
        self.image_frame.apply_ovals()

    def onClickAgregar(self):
        if self.areAllParamsDisplayedValid():
            Intensidad = self.displayed_elipse.Intensidad
            SemiEjeX = self.displayed_elipse.SemiEjeX
            SemiEjeY = self.displayed_elipse.SemiEjeY
            CentroX = self.displayed_elipse.CentroX
            CentroY = self.displayed_elipse.CentroY
            Inclinacion = self.displayed_elipse.Inclinacion
            new_elipse = elipse(Intensidad,SemiEjeX,SemiEjeY,CentroX,CentroY,Inclinacion)
            self.elipse_list.append(new_elipse)
            self.update_text()

            self.updateElipseGraphics()
            self.update_plot(self.image_frame.image)
        else:
            print("error en alguno de los parametros")

    def onClickBorrar(self):
        if len(self.elipse_list) > 0:
            self.elipse_list.pop()
            self.update_text()
        else:
            #que no haga nada cuando esta vacia
            pass

    def update_text(self):
        tableStr = ""
        for elip in self.elipse_list:
            tableStr+= elip.str_with_params()+ "\n"
        self.textEditParametersChart.setText(tableStr)

    #escribimos la validacion del numero de la funcion asociada al evento textChanged
    def validateNumberIntensidad(self):
        if self.displayed_elipse.Intensidad is not None:
            if  -1.0 <=self.displayed_elipse.Intensidad <= 1.0:
                return True
            else:
                print("rango invalido de Intensidad")
                return False
        else:
            return False
    def validateNumberSemiEjeX(self):
        #sobreescribir con rango
        if self.displayed_elipse.SemiEjeX is not None:
            return True
        else:
            return False
    def validateNumberSemiEjeY(self):
        #sobreescribir con rango
        if self.displayed_elipse.SemiEjeY is not None:
            return True
        else:
            return False
    def validateNumberCentroX(self):
        #sobreescribir con rango
        if self.displayed_elipse.CentroX is not None:
            return True
        else:
            return False
    def validateNumberCentroY(self):
        #sobreescribir con rango
        if self.displayed_elipse.CentroY is not None:
            return True
        else:
            return False
    def validateNumberInclinacion(self):
        #sobreescribir con rango
        if self.displayed_elipse.Inclinacion is not None:
            return True
        else:
            return False

    #escribimos la funcion asociada al evento textChanged
    def textChangedIntensidad(self):
        if(self.lineEditIntensidad.text()=='.'):
            self.displayed_elipse.Intensidad = 0
        else:
            if(len(self.lineEditIntensidad.text())!=0):
                input_number = float(self.lineEditIntensidad.text())
                self.displayed_elipse.Intensidad = input_number
    def textChangedSemiEjeX(self):
        if(self.lineEditSemiEjeX.text()=='.'):
            self.displayed_elipse.SemiEjeX = 0
        else:
            if(len(self.lineEditSemiEjeX.text())!=0):
                input_number = int(self.lineEditSemiEjeX.text())
                self.displayed_elipse.SemiEjeX = input_number
    def textChangedSemiEjeY(self):
        if(self.lineEditSemiEjeY.text()=='.'):
            self.displayed_elipse.SemiEjeY = 0
        else:
            if(len(self.lineEditSemiEjeY.text())!=0):
                input_number = int(self.lineEditSemiEjeY.text())
                self.displayed_elipse.SemiEjeY = input_number
    def textChangedCentroX(self):
        if(self.lineEditCentroX.text()=='.'):
            self.displayed_elipse.CentroX = 0
        else:
            if(len(self.lineEditCentroX.text())!=0):
                input_number = int(self.lineEditCentroX.text())
                self.displayed_elipse.CentroX = input_number
    def textChangedCentroY(self):
        if(self.lineEditCentroY.text()=='.'):
            self.displayed_elipse.CentroY = 0
        else:
            if(len(self.lineEditCentroY.text())!=0):
                input_number = int(self.lineEditCentroY.text())
                self.displayed_elipse.CentroY = input_number
    def textChangedInclinacion(self):
        if(self.lineEditInclinacion.text()=='.'):
            self.displayed_elipse.Inclinacion = 0
        else:
            if(len(self.lineEditInclinacion.text())!=0):
                input_number = float(self.lineEditInclinacion.text())
                self.displayed_elipse.Inclinacion = input_number
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()