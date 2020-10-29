from gui_radon import *
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        #self.plot()
 
 
    def plot(self):
        x = np.array([50, 30,40])
        labels = ["Apples", "Bananas", "Melons"]
        ax = self.figure.add_subplot(111)
        ax.pie(x, labels=labels) 

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
        
        top = 400
        left = 400
        width = 900
        height = 500
        self.setGeometry(top, left, width, height)
        self.elipse_list = []

        self.displayed_elipse = elipse()


        canvas = Canvas(self, width=3, height=2)
        canvas.move(400,50)


        #asignamos la funcion asociada al evento textChanged
        self.lineEditIntensidad.textChanged.connect(self.textChangedIntensidad)
        self.lineEditIntensidad.setValidator(QtGui.QDoubleValidator(1.0,-1.0,4))
        self.lineEditSemiEjeX.textChanged.connect(self.textChangedSemiEjeX)
        self.lineEditSemiEjeY.textChanged.connect(self.textChangedSemiEjeY)
        self.lineEditCentroX.textChanged.connect(self.textChangedCentroX)
        self.lineEditCentroY.textChanged.connect(self.textChangedCentroY)
        self.lineEditInclinacion.textChanged.connect(self.textChangedInclinacion)

        #self.textEditIntensidad.setVali

#        self.pushButton.setText("Presióname")
        #asignamos la funcion asociada al evento clicked en push buttons
        self.pushButtonAgregar.clicked.connect(self.onClickAgregar)
        self.pushButtonBorrar.clicked.connect(self.onClickBorrar)


    def areAllParamsDisplayedValid(self):
        if(self.validateNumberIntensidad() and self.validateNumberSemiEjeX() and self.validateNumberSemiEjeY()
        and self.validateNumberCentroX() and self.validateNumberCentroY() and self.validateNumberInclinacion()):
            return True
        else:
            return False
        #escribimos la funcion asociada al evento clicked en push buttons
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
        if(len(self.lineEditIntensidad.text())!=0):
            input_number = float(self.lineEditIntensidad.text())
            self.displayed_elipse.Intensidad = input_number
    def textChangedSemiEjeX(self):
        input_number = float(self.lineEditIntensidad.text())
        self.displayed_elipse.SemiEjeX = input_number
    def textChangedSemiEjeY(self):
        input_number = float(self.lineEditIntensidad.text())
        self.displayed_elipse.SemiEjeY = input_number
    def textChangedCentroX(self):
        input_number = float(self.lineEditIntensidad.text())
        self.displayed_elipse.CentroX = input_number
    def textChangedCentroY(self):
        input_number = float(self.lineEditIntensidad.text())
        self.displayed_elipse.CentroY = input_number
    def textChangedInclinacion(self):
        input_number = float(self.lineEditIntensidad.text())
        self.displayed_elipse.Inclinacion = input_number
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()