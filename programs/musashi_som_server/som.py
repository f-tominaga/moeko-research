# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.filedialog

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

if __name__=='__main__':
    print('Try to load T-SOM')
    som = SOM()
    som.open()
