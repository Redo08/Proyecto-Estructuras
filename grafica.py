import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mi primera App con PyQt5")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()

        self.label = QLabel("¡Hola, PyQt5!", self)
        self.layout.addWidget(self.label)

        self.boton = QPushButton("Haz clic", self)
        self.boton.clicked.connect(self.cambiar_texto)
        self.layout.addWidget(self.boton)

        self.setLayout(self.layout)

    def cambiar_texto(self):
        self.label.setText("¡Botón presionado!")

app = QApplication(sys.argv)
ventana = MiVentana()
ventana.show()
sys.exit(app.exec_())