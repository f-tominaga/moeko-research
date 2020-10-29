# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.filedialog
import numpy as np

class SOM:
    def __init__(self,):
        print('create SOM instance')

    def open(self,):
        root = tkinter.Tk()
        root.withdraw()
        ftype = [("","*.csv")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.file = tkinter.filedialog.askopenfilename(filetypes = ftype,
                                                  initialdir = iDir)

        #make som instance
        self.tensor = np.loadtxt(self.file, delimiter=',')
        self.tensor = self.tensor.reshape((100, 100, 3))

        print(self.tensor.shape)
        #load SOM from csv file


if __name__=='__main__':
    print('Try to load T-SOM')
    som = SOM()
    som.open()
