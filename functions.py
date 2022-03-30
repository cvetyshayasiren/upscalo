import os
import subprocess
import traceback

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QGroupBox, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5 import QtWidgets
from PyQt5.uic.properties import QtGui


def warnings(title=str, text=str, icon=QMessageBox.Warning):  # всплывающее окно
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.exec_()


def add_picture(file, context):
    pix = QPixmap(file)
    item = QtWidgets.QGraphicsPixmapItem(pix)
    scene = QtWidgets.QGraphicsScene(context)
    scene.addItem(item)
    return scene

def update_scroll(self):
    print("try to update")
    scroll = self.ui.QScrollAreaPictures
    scroll.setWidgetResizable(True)
    groupBox = QGroupBox()
    hbox = QHBoxLayout()
    files = os.listdir("inputs")
    for i in files:
        widget = QLabel(self)
        widget.setPixmap(QPixmap(f"inputs/{i}").scaledToHeight(scroll.height() - 20))
        hbox.addWidget(widget)

    groupBox.setLayout(hbox)
    scroll.setWidget(groupBox)
    print("updated")

def test(self):
    while True:
        print(self.ui.scrollAreaPictures.height())
        import time
        time.sleep(1)

def update_model_choice(self, mode = 'upscale'):
    if str(mode) not in ('upscale', 'face'):
        return
    path = ''
    if str(mode) == 'upscale':
        path = 'Real-ESRGAN\experiments\pretrained_models'
    if str(mode) == 'face':
        path = 'GFPGAN\experiments\pretrained_models'

    models = [i for i in os.listdir(path) if i.endswith('.pth')]
    self.ui.comboBox_model.clear()
    for i in models:
        self.ui.comboBox_model.addItem(i)
    print('Список моделей обновлён')

def work(arg, self):
    subprocess.run(arg)
    files = os.listdir("results")
    for i in files:
        self.ui.graphicsView_after.setScene(add_picture("results/" + i, self))

