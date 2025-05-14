#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 11:59:52 2025

@author: diego
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path = 'cold_teottom/IV_cold_92_75_94_65_85_quadrant_4s.csv'
save_path = 'cold_tests/splitted_data/Bottom/quadrants'

data = pd.read_csv(data_path)
data = data.apply(pd.to_numeric, errors = 'coerce')

def split(data, quadrants_in = False, tiles_in = False, vPDUchan_in = False, tiles_ana = False, save_path = 'test_f'):
    
    quadrants = quadrants_in or ['1', '2', '3', '4']
    tiles = tiles_in or ['1', '2', '3', '4']
    vPDUchan = vPDUchan_in or ['0', '1', '2', '3', '4']
    i = 0
    
    for quadrant in quadrants:    
        if tiles_ana:
            for tile in tiles:
                for chan in vPDUchan:
                    dt = data[data['Tile'] == float(quadrant + '.' + tile)]
                    voltage = dt['CAEN' + chan + '_Voltage (V)']
                    current = dt['CAEN' + chan + '_Current (uA)']
        
                    tosave = np.vstack((voltage, current)).T
                    np.savetxt(f'{save_path}/tiles_ch' + str(i) + '.csv', tosave, delimiter=',')
                    i = i + 1
        else:
            for chan in vPDUchan:
                dt = data[data['Tile'] == float(quadrant + '.')]
                voltage = dt['CAEN' + chan + '_Voltage (V)']
                current = dt['CAEN' + chan + '_Current (uA)']
    
                tosave = np.vstack((voltage, current)).T
                np.savetxt(f'{save_path}/tiles_ch' + str(i) + '.csv', tosave, delimiter=',')
                i = i + 1

"""
#EXAMPLES =====================================================================
#Case for all the tiles
split(data, tiles_ana = True, save_path = save_path)
#Case for the quadrants
split(data, tiles_ana = False, save_path = save_path)
#Selecting a specific vPDU and all the tiles
split(data, tiles_ana = True, vPDUchan_in= '0', save_path = save_path)
#Selecting a specific quadrant for all the tilevPDUs
split(data, tiles_ana = False, quadrants_in= '2', save_path = save_path)
#........
"""