#pyuic5 interface.ui -o interface.py
import os
import shutil
import subprocess
import threading
import traceback

from PyQt5.uic.properties import QtCore

from functions import warnings, add_picture, update_scroll, update_model_choice, work
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from interface import Ui_MainWindow
from signals import *
import sys


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_start.clicked.connect(self.pushButton_start)
        self.ui.pushButton_add_photo.clicked.connect(self.pushButton_add_photo)

        self.ui.radioButton_upscale.clicked.connect(self.radioButton_upscale)
        self.ui.radioButton_face.clicked.connect(self.radioButton_face)

        self.ui.pushButton_add_model.clicked.connect(self.pushButton_add_model)

        update_model_choice(self)
        print("Upscalo is running")

    def showEvent(self, show):
        update_scroll(self)

    def keyPressEvent(self, key):
        print(key.key())

    def pushButton_add_model(self):
        file = QFileDialog.getOpenFileName()[0]
        models = [os.listdir("Real-ESRGAN\experiments\pretrained_models"), os.listdir("GFPGAN\experiments\pretrained_models")]
        print(file.split('/')[-1])
        print(models)
        if str(file.split('/')[-1]) in str(models):
            warnings('Ой', 'Эта модель уже загружена.')
            return

        if 'RealESRGAN' in file and file.endswith('.pth'):
            shutil.copyfile(file, f"Real-ESRGAN\experiments\pretrained_models\\{file.split('/')[-1]}")

        elif 'GFPGAN' in file and file.endswith('.pth'):
            shutil.copyfile(file, f"GFPGAN\experiments\pretrained_models\\{file.split('/')[-1]}")
        else:
            warnings('Внимание!', 'Имя должно содержать "RealESRGAN" или "GFPGAN", а разрешение файла должно быть .pth')
            return
        print('Модель загружена')
        update_model_choice(self)


    def radioButton_upscale(self):
        update_model_choice(self, 'upscale')


    def radioButton_face(self):
        update_model_choice(self, 'face')


    def pushButton_add_photo(self):
        file = QFileDialog.getOpenFileName()[0]
        if file == '':
            warnings("Ой", "Файл не выбран🤷‍", QMessageBox.Information)
            return
        try:
            shutil.copyfile(file, f"inputs/{file.split('/')[-1]}")
        except Exception as er:
            print(er)
            print(traceback.format_exc())
        if '.jpg' not in str(file) and '.png' not in str(file):
            warnings("Внимание!", "Файл должен быть в формате JPG или PNG")
            return
        self.ui.graphicsView_before.setScene(add_picture(file, self))

        update_scroll(self)

    def pushButton_start(self):
        print("running...")
        import shlex

        model = self.ui.comboBox_model.currentText()
        print(model)

        if self.ui.radioButton_upscale.isChecked():
            arg = shlex.split(f"python Real-ESRGAN/inference_realesrgan.py "
                              f"--model_path Real-ESRGAN/experiments/pretrained_models/{model} "
                              f"--input inputs "
                              f"--output results "
                              f"--face_enhance")
        else:
            arg = shlex.split(f"python GFPGAN/inference_gfpgan.py --upscale 2 --test_path inputs --save_root results")

        threading.Timer(0, work, [arg, self]).start()
        print('aga')


def start():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        print("Error: \n" + str(e) + "\n\nTraceback: \n" + str(traceback.format_exc()))
