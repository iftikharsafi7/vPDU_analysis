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

def split(data, quadrants_in = False, tiles_in = False, vPDUchan_in = False, tiles_ana = False, save = True, save_path = 'test_f'):
    """
    - OLD VERSION: This version allows for more inputs being able to select 
    specific channles and tiles to run the script but it doesn't work properly 
    in the Jupyter Notebook. 
    It might be useful for detailed analysis but for regular analysis I 
    recommend to use split_v2.
    
    - FIXME: This function requires rework and rename of the variables and 
    inputs as well !!
    """
    quadrants = quadrants_in or ['1', '2', '3', '4']
    tiles = tiles_in or ['1', '2', '3', '4']
    vPDUchan = vPDUchan_in or ['0', '1', '2', '3', '4']
    i = 0
    
    if tiles_ana:
        for chan in vPDUchan:
            for quadrant in quadrants:
                for tile in tiles:
                    dt = data[data['Tile'] == float(quadrant + '.' + tile)]
                    voltage = dt['CAEN' + chan + '_Voltage (V)']
                    current = dt['CAEN' + chan + '_Current (uA)']
                    if save == True:
                        tosave = np.vstack((voltage, current)).T
                        print(tosave)
                        if tosave.size != 0:
                            np.savetxt(f'{save_path}/IV_q' + str(i) + '.txt', tosave, delimiter=',')
                            i = i + 1
    else:
        for chan in vPDUchan:
            for quadrant in quadrants: 
                dt = data[data['Tile'] == float(quadrant + '.')]
                voltage = dt['CAEN' + chan + '_Voltage (V)']
                current = dt['CAEN' + chan + '_Current (uA)']
                if save == True:
                    tosave = np.vstack((voltage, current)).T
                    if tosave.size != 0:
                        np.savetxt(f'{save_path}/IV_q' + str(i) + '.txt', tosave, delimiter=',')
                        i = i + 1


def split_v2(df, offset = 2.6, save=False, save_path=None):
    # Applying offset before the splitting    
    voltage_cols = [col for col in df.columns if 'Voltage' in col]
    df[voltage_cols] = df[voltage_cols] + offset
    #Select columns and splitting
    columns_to_group = df.columns[1:]
    unique_tiles = df['Tile'].unique()
    
    j = 0
    for tile in unique_tiles:
        
        tile_data = df[df['Tile'] == tile]
        for i in range(0, len(columns_to_group), 2):
            group = columns_to_group[i:i+2]
            reversed_group = list(group[::-1])
            
            subset = tile_data[reversed_group]
            
            if save:
                filename = f"{save_path}/IV_q{j}.txt" if save_path else f"IV_q{j}.txt"
                subset.to_csv(filename, sep=',', index=False, header = None)
                j += 1

if __name__ == "__main__":
    data_path = '../vPDU_apr-may25/Batch_2/warm_tests/Data/IV/IV_warm_98_57_83_quadrants_23052025_3s.csv'
    save_path = '../vPDU_apr-may25/Batch_2/warm_tests/Data/IV/splitted/'
    
    data = pd.read_csv(data_path)
    data = data.apply(pd.to_numeric, errors = 'coerce')
    data = data[(data['CAEN0_Voltage (V)'] >= 35) & (data['CAEN1_Voltage (V)'] >= 35) & (data['CAEN2_Voltage (V)'] >= 35) ]#& (df['CAEN3_Voltage (V)'] >= 35) & (df['CAEN4_Voltage (V)'] >= 35)]





#EXAMPLES =====================================================================
#Case for all the tiles
"""
split(data, tiles_ana = True, save_path = save_path)
#Case for the quadrants
split(data, tiles_ana = False, save_path = save_path)
#Selecting a specific vPDU and all the tiles
split(data, tiles_ana = True, vPDUchan_in= '0', save_path = save_path)
#Selecting a specific quadrant for all the tilevPDUs
split(data, tiles_ana = False, quadrants_in= '2', save_path = save_path)
#........

#split(data, tiles_ana = True, vPDUchan_in= '0', save_path = save_path)

split(data, tiles_ana = True,  vPDUchan_in= ['0', '1', '2'], save_path = save_path)
"""