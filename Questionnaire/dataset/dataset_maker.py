# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import tkinter.filedialog
import os
import csv

OUTPUT = './deformated.txt'

if __name__=="__main__":
    print('dataset maker')
    
    root = tkinter.Tk()
    root.withdraw()
    fType = [("dataset","txt")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfile(filetype=fType, initialdir=iDir)
    print('file >>', file_name.name)
    
    #
    # raw data set object
    #
    dataset = []
    new_data_format = []

    with open(file_name.name,'r',encoding='utf-8') as f:
        lines = f.readlines()
        print("lines:", len(lines))
        
        for line in lines:
            if line[0] == '#':
                continue;
            
            elems = line.strip('\n').split('\t')
            dataset.append(elems)   
            # print(dataset)
        
        # dataset = [dat[1:] for dat in dataset[0:]]
        # dataset = np.array(dataset)
        print("RAW >>")
        print(np.array(dataset))
        print('')
    
        #role clip
        alpha_set = []
        beta_set = []
        gamma_set = []
        for dat in dataset:
            if dat[0] == str('α'):
                alpha_set.append(dat[2:])
                # print(dat)
            if dat[0] == str('β'):
                beta_set.append(dat[2:])
            if dat[0] == str('γ'):
                gamma_set.append(dat[2:])
                
        # print(np.array(alpha_set))       
        
        
        for dat in alpha_set:
            tmp = dat[6:8]
            tmp  = tmp + dat[:6]
            tmp = tmp + dat[15:17]
            tmp = tmp + dat[8:15]
            new_data_format.append(tmp)
        for dat in beta_set:
            tmp = dat[6:8]
            tmp  = tmp + dat[:6]
            tmp = tmp + dat[15:17]
            tmp = tmp + dat[8:15]
            new_data_format.append(tmp)
        for dat in gamma_set:
            tmp = dat[6:8]
            tmp  = tmp + dat[:6]
            tmp = tmp + dat[15:17]
            tmp = tmp + dat[8:15]
            new_data_format.append(tmp)
            
        print('deformed >>')
        print(np.array(new_data_format))
        
    #write to file
    with open(OUTPUT,'w',encoding='utf-8') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows(new_data_format)
    
    print('Finish!!!')
        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
