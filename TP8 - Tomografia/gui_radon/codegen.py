def textChangedIntensidad(self):
    if(len(self.lineEditIntensidad.text())!=0):
        input_number = float(self.lineEditIntensidad.text())
        self.displayed_elipse.Intensidad = input_number
def textChangedSemiEjeX(self):
    if(len(self.lineEditSemiEjeX.text())!=0):
        input_number = int(self.lineEditSemiEjeX.text())
        self.displayed_elipse.SemiEjeX = input_number
def textChangedSemiEjeY(self):
    if(len(self.lineEditSemiEjeY.text())!=0):
        input_number = int(self.lineEditSemiEjeY.text())
        self.displayed_elipse.SemiEjeY = input_number
def textChangedCentroX(self):
    if(len(self.lineEditCentroX.text())!=0):
        input_number = int(self.lineEditCentroX.text())
        self.displayed_elipse.CentroX = input_number
def textChangedCentroY(self):
    if(len(self.lineEditCentroY.text())!=0):
        input_number = int(self.lineEditCentroY.text())
        self.displayed_elipse.CentroY = input_number
def textChangedInclinacion(self):
    if(len(self.lineEditInclinacion.text())!=0):
        input_number = float(self.lineEditInclinacion.text())
        self.displayed_elipse.Inclinacion = input_number