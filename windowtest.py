from PyQt6.QtWidgets import QWidget, QMainWindow,QApplication, QLabel, QGraphicsView, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap, QImage
import os

path=os.path.dirname(os.path.abspath(__file__))

print(path)
app=QApplication([])


q=QWidget()

label=QLabel()

image=QImage()
image.load('H6.png')

label.setPixmap(QPixmap.fromImage(image))


layout=QVBoxLayout()
layout.addWidget(label)
#layout.addWidget(image)

q.setLayout(layout)
q.show()
app.exec()
