# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.filedialog
import numpy as np
import json
#from musashi_som_server import tsom2_viewer as TSOM2_V
import tsom2_viewer as TSOM2_V

class SOM:
    def __init__(self,):
        print('create SOM instance')

    def open(self, cfg_file:str):              
        #Load config file
        json_file = open(cfg_file)
        json_data = json.load(json_file)
        print('Config:{}'.format(json_data))
        mode1_model_file = os.path.abspath(json_data['mode1_model'])
        mode2_model_file = os.path.abspath(json_data['mode2_model'])
        som_model_file = os.path.abspath(json_data['som_model'])
        label_path1 = os.path.abspath(json_data['label1'])
        label_path2 = os.path.abspath(json_data['label2'])
        label_path3 = os.path.abspath(json_data['label3'])


        # make som models
        self.model = np.loadtxt(som_model_file, delimiter=',')
        self.bmu1 = np.loadtxt(mode1_model_file, delimiter=',')
        self.bmu2 = np.loadtxt(mode2_model_file, delimiter=',')
        
        self.model = self.model.reshape((100, 100, 3))
        self.bmu1 = np.int64(np.round(self.bmu1))
        self.bmu2 = np.int64(np.round(self.bmu2))
        print('bmu1:', self.bmu1)
        print('bmu2:', self.bmu2)

        label1 = np.genfromtxt(label_path1, dtype=str)
        label2 = np.genfromtxt(label_path2, dtype=str)
        label3 = np.genfromtxt(label_path3, dtype=str)
        print('Label1:', label1)
        print('Label2:', label2)
        print('Label3:', label3)

        # Viewer's setting
        # comp = TSOM2_V.TSOM2_Viewer(y=self.model,
        #                             winner1=self.bmu1, 
        #                             winner2=self.bmu2,
        #                             label2=label2, 
        #                             button_label=label3)
        # comp.draw_map()

        print(self.model.shape)


if __name__ == '__main__':
    print('Try to load T-SOM')
    som = SOM()
    som.open('cfg/test.json')
