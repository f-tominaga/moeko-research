# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.filedialog
import numpy as np
from musashi_som_server import tsom2_viewer as TSOM2_V

class SOM:
    def __init__(self,):
        print('create SOM instance')

    def open(self,):
        root = tkinter.Tk()
        root.withdraw()
        ftype = [("","*.csv")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file1 = tkinter.filedialog.askopenfilename(filetypes=ftype,
                                                       initialdir=iDir)
        file2 = tkinter.filedialog.askopenfilename(filetypes=ftype,
                                                       initialdir=iDir)
        file3 = tkinter.filedialog.askopenfilename(filetypes=ftype,
                                                       initialdir=iDir)

        # make som instance
        self.tensor = np.loadtxt(file1, delimiter=',')
        self.bmu1 = np.loadtxt(file2, delimiter=',')
        self.bmu2 = np.loadtxt(file3, delimiter=',')
        self.bmu1 = np.int64(np.round(self.bmu1))
        self.bmu2 = np.int64(np.round(self.bmu2))

        dir_name = 'data'
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        label_name1 = 'Label_3600.txt'
        label_path1 = os.path.join(dir_path, label_name1)
        label_name2 = 'Label_7.txt'
        label_path2 = os.path.join(dir_path, label_name2)
        label_name3 = 'Label_3.txt'
        label_path3 = os.path.join(dir_path, label_name3)
        label1 = np.genfromtxt(label_path1, dtype=str)
        label2 = np.genfromtxt(label_path2, dtype=str)
        label3 = np.genfromtxt(label_path3, dtype=str)
        print('bmu1', self.bmu1)
        print('bmu2', self.bmu2)

        # comb
        self.tensor = self.tensor.reshape((100, 100, 3))

        # Viewer's setting
        comp = TSOM2_V.TSOM2_Viewer(y=self.tensor, winner1=self.bmu1, winner2=self.bmu2,
                                    label2=label2, button_label=label3)

        # マップ表示です
        comp.draw_map()

        print(self.tensor.shape)
        #load SOM from csv file


if __name__ == '__main__':
    print('Try to load T-SOM')
    som = SOM()
    som.open()
    print('Finshi all tasts')
