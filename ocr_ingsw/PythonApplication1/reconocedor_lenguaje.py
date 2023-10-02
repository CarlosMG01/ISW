#Hay que instalar las librerías: tesseract y PyQt5

import pytesseract
from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class FileDialogExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Selección de Archivo')

        self.button = QPushButton('Seleccionar Archivo', self)
        self.button.setGeometry(150, 80, 200, 40)
        self.button.clicked.connect(self.showDialog)

        self.selected_file_label = self.statusBar()

    def showDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, 'Seleccionar Archivo PNG', '', 'Imágenes PNG (*.png);;', options=options)

        if file_name:
            # Utiliza pytesseract para extraer texto de la imagen
            texto_extraido = pytesseract.image_to_string(file_name)

            # Imprime el texto extraído
            print(texto_extraido)
            
            self.close() #Cierra la ventana

def main():
    app = QApplication(sys.argv)
    ex = FileDialogExample()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

