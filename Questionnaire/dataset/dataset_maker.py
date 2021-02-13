# -*- coding: utf-8 -*-
"""
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tkinter.filedialog
import os
import csv

OUTPUT = './deformated.txt'
NPY_OUTPUT = 'robot.npy'

if __name__=="__main__":
    print('dataset maker')
    
    root = tkinter.Tk()
    root.withdraw()
    fType = [("dataset","txt")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_path = tkinter.filedialog.askopenfile(filetype=fType, initialdir=iDir)
    
    print('File >>', file_path.name)
    
    #------------------------------
    # raw data set object
    #------------------------------
    raw_data = np.genfromtxt(fname=file_path.name,
        dtype=None,
        names=['role','situ',
                'bx','by','ax','ay','bx','by','cx','cy','d',
                'wl','t',
                'shoot','pass','ballget','clear','active','cover','waitpass'],
        encoding='utf-8',delimiter='\t',comments='#')

    # print(raw_data)


    #------------------------------
    # extraction alpha dataset
    #------------------------------
    alpha_data = []
    beta_data = []
    gamma_data = []
    for dat in raw_data:
        if dat[0] == 'α':
            tmp = [v for v in dat]
            alpha_data.append(tmp[2:])
        if dat[0] == 'β':
            tmp = [v for v in dat]
            beta_data.append(tmp[2:])
        if dat[0] == 'γ':
            tmp = [v for v in dat]
            gamma_data.append(tmp[2:])

    alpha_data = np.array(alpha_data)
    beta_data = np.array(beta_data)
    gamma_data = np.array(gamma_data)



    print('Alpha {} >>'.format(len(alpha_data)*18))
    # print(alpha_data)

    #
    # change shape for T-SOM
    #
    alpha_data  = alpha_data.flatten(order='F')
    beta_data   = beta_data.flatten(order='F')
    gamma_data  = gamma_data.flatten(order='F')
    # np.savetxt('test.txt', tmp, encoding='utf-8')

    #titin puipui
    alpha_data = np.reshape(alpha_data, (-1, 1))
    beta_data = np.reshape(beta_data, (-1, 1))
    gamma_data = np.reshape(gamma_data, (-1, 1))
    # print(alpha_data.shape)

    train_data = np.hstack([alpha_data, beta_data])
    train_data = np.hstack([train_data, gamma_data])
    print('Stacked {}'.format(train_data.shape))

    PARAM_NUM = 18
    PRODUCT_NUM = 270
    ROLE_NUM = 3
    print(PARAM_NUM, PRODUCT_NUM, ROLE_NUM)
    train_data = np.reshape(train_data,(PARAM_NUM, PRODUCT_NUM, ROLE_NUM))

    print("TRAIN DATA {} >>".format(train_data.shape))
    # print(train_data)

    train_data = np.transpose(train_data, (1,2,0))

    #debug
    print(train_data[:,0,11]-train_data[:,1,11])

    print("TRANSPOSED {} >>".format(train_data.shape))
    # print(train_data)

    #------------------------------
    # save to npy
    #------------------------------    
    np.save(NPY_OUTPUT, train_data)



        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
