#This script has the tiles data in each quadrant, and also for a single quadrant. 
script for Tiles #comment in case of quadrant, uncomment in case of tiles
import concurrent.futures
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ks_2samp
from datetime import date


def calculate_breakdown_voltage(I, V, R=1, f_thr=4, x_min=50, x_max=200):
    # Filter for the desired range in V
    indices = (V >= x_min) & (V <= x_max)
    V_filtered = V[indices]
    I_filtered = I[indices]

    dydx = np.diff(np.log(I_filtered)) / np.diff(V_filtered)
    ry = dydx[0:-1].reshape(-1, R).mean(axis=1)
    rx = V_filtered[1:-1].reshape(-1, R).mean(axis=1)

    mean = np.mean(ry[0:10])
    i = np.argwhere(ry > f_thr * mean)

    if len(i) > 0:
        i = i[0][0]
    else:
        print("No range found where derivative exceeds threshold")
        return None, None

    Vbd = rx[i]
    d_Vbd = Vbd * mean * f_thr / np.sqrt(10)
    return Vbd, round(d_Vbd, 1)


def plot_IV_data(file_path, tile, ax, x_min=50, x_max=200):
    try:
        if powersupply == 'k':
            data = np.genfromtxt(file_path, delimiter=',')
            x = data[:, 0]+2.6
            y = data[:, 1]
        else:
            x = file_path['Voltage (V)'].to_numpy()+2.6
            y = file_path['Current (uA)'].to_numpy()

        # Filter based on the specified x range
        x_filtered = x[(x >= x_min) & (x <= x_max)]
        y_filtered = y[(x >= x_min) & (x <= x_max)]

        bdv, err_vbd = calculate_breakdown_voltage(y_filtered, x_filtered, x_min=x_min, x_max=x_max)
        if bdv is not None:
            ax.axvline(bdv, linestyle='dashed')
            ax.plot(x, y * 1e6, label=f'{tile} bdv: {round(bdv, 1)} +/- {err_vbd} V')
            ax.set_xlabel('Voltage (V)')
            ax.set_ylabel('Current (uA)')
            ax.legend(loc='upper left', prop={'size': 6})
        else:
            ax.plot(x, y * 1e6, label=f'{tile} bdv: None +/- None V')
            #ax.plot(x, y * 1e6, label=f'{tile} bdv: {round(bdv, 1)} +/- {err_vbd} V')
            ax.set_xlabel('Voltage (V)')
            ax.set_ylabel('Current (uA)')
            ax.legend(loc='upper left', prop={'size': 6})
            #ax.set_facecolor('red')
    except OSError:
        print(f"Warning: Failed to read file: {file_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--Input", help="Directory/to/data/for/IV")
    parser.add_argument("-PS", "--PowerSupply", help="Power supply used to take IVs. (C)aen or (K)eithly")
    parser.add_argument("--x_min", type=float, default=51, help="Minimum voltage range for analysis")
    parser.add_argument("--x_max", type=float, default=200, help="Maximum voltage range for analysis")
    args = parser.parse_args()

    filepath = args.Input
    powersupply = args.PowerSupply
    x_min = args.x_min
    x_max = args.x_max

    IV_file = [f'ivcurve{i}.txt' for i in range(20)]

    if powersupply == 'k':
        plt.rcParams.update({'font.size': 8})
        figIV, axIV = plt.subplots(2, 2, figsize=(8, 8))

        for i in range(4):
            plot_IV_data(filepath + IV_file[i], i, axIV[0, 0], x_min, x_max)
            axIV[0, 0].set_title('Quadrant 1')

        for i in range(4, 8):
            plot_IV_data(filepath + IV_file[i], i, axIV[0, 1], x_min, x_max)
            axIV[0, 1].set_title('Quadrant 2')

        for i in range(8, 12):
            plot_IV_data(filepath + IV_file[i], i, axIV[1, 0], x_min, x_max)
            axIV[1, 0].set_title('Quadrant 3')

        for i in range(12, 16):
            plot_IV_data(filepath + IV_file[i], i, axIV[1, 1], x_min, x_max)
            axIV[1, 1].set_title('Quadrant 4')

        # Optionally add plots for summary data in each quadrant
        plot_IV_data(filepath + IV_file[16], 'quad 1 sum', axIV[0, 0], x_min, x_max)
        plot_IV_data(filepath + IV_file[17], 'quad 2 sum', axIV[0, 1], x_min, x_max)
        plot_IV_data(filepath + IV_file[18], 'quad 3 sum', axIV[1, 0], x_min, x_max)
        plot_IV_data(filepath + IV_file[19], 'quad 4 sum', axIV[1, 1], x_min, x_max)

        plt.tight_layout()
        plt.show()

    if powersupply == 'c':
        df = pd.read_csv(filepath)
        plt.rcParams.update({'font.size': 8})
        figIV, axIV = plt.subplots(2, 2, figsize=(8, 8))

        for i in range(1, 5):
            plot_IV_data(df[(df['Quadrant'] == 1) & (df['Tile'] == i)], i, axIV[0, 0], x_min, x_max)
            axIV[0, 0].set_title('Quadrant 1')

        for i in range(1, 5):
            plot_IV_data(df[(df['Quadrant'] == 2) & (df['Tile'] == i)], i, axIV[0, 1], x_min, x_max)
            axIV[0, 1].set_title('Quadrant 2')

        for i in range(1, 5):
            plot_IV_data(df[(df['Quadrant'] == 3) & (df['Tile'] == i)], i, axIV[1, 0], x_min, x_max)
            axIV[1, 0].set_title('Quadrant 3')

        for i in range(1, 5):
            plot_IV_data(df[(df['Quadrant'] == 4) & (df['Tile'] == i)], i, axIV[1, 1], x_min, x_max)
            axIV[1, 1].set_title('Quadrant 4')

        # Optional sum plot code, uncomment if needed
        # plot_IV_data(df[(df['Quadrant'] == 1) & (df['Tile'] == 1234)], 'quad 1 sum', axIV[0, 0], x_min, x_max)
        # plot_IV_data(df[(df['Quadrant'] == 2) & (df['Tile'] == 1234)], 'quad 2 sum', axIV[0, 1], x_min, x_max)
        # plot_IV_data(df[(df['Quadrant'] == 3) & (df['Tile'] == 1234)], 'quad 3 sum', axIV[1, 0], x_min, x_max)
        # plot_IV_data(df[(df['Quadrant'] == 4) & (df['Tile'] == 1234)], 'quad 4 sum', axIV[1, 1], x_min, x_max)

        plt.tight_layout()
        plt.show()



#script for Quadrant
# import concurrent.futures #import used to parallelise analysis
# import argparse
# import ast
# import glob
# import csv
# import numpy as np
# import pandas as pd
# import subprocess
# import matplotlib
# import matplotlib.pyplot as plt
# from datetime import date
# from scipy import stats
# from scipy.stats import ks_2samp
# from scipy.stats import kstest, norm
# from scipy.stats import norm
# from scipy.signal import savgol_filter as savgol

# import csv
# from scipy import interpolate


# def calculate_breakdown_voltage(I, V, R=1, f_thr=3):
#     dydx = np.diff(np.log(I)) / np.diff(V)
#     ry = dydx[0:-1].reshape(-1, R).mean(axis=1)
#     rx = V[1:-1].reshape(-1, R).mean(axis=1)
#     mean = np.mean(ry[0:10])
#     i = np.argwhere(ry > f_thr * mean)
#     if len(i) > 0:
#         i = i[0][0]
#     else:
#         print("No range found where derivative exceeds threshold")
#         return None, None
#     Vbd = rx[i]
#     d_Vbd = Vbd * mean * f_thr / np.sqrt(10)
#     return Vbd, round(d_Vbd, 1)

# def plot_IV_data(file_path,tile ,ax):
#     try:
#         if powersupply == 'k':
#             data = np.genfromtxt(file_path, delimiter=',')
#             x = data[:, 0]
#             y = data[:, 1]
#         else:
#             x = file_path['Voltage (V)'].to_numpy()
#             y = file_path['Current (uA)'].to_numpy()
#         x_filtered = x[x > 40]
#         y_filtered = y[x > 40]
#         bdv, err_vbd = calculate_breakdown_voltage(y_filtered, x_filtered)
#         if bdv is not None:
#             ax.axvline(bdv,linestyle='dashed')
#             ax.plot(x, y * 1e6, label=f'{tile} bdv: {bdv} +/- {err_vbd} V')
#             ax.set_xlabel('Voltage (V)')
#             ax.set_ylabel('Current (uA)')
#             ax.legend(loc='upper left', prop={'size': 12})
#         else:
#             ax.plot(x, y * 1e6, label=f'{tile} bdv: {bdv} +/- {err_vbd} V')
#             ax.set_xlabel('Voltage (V)')
#             ax.set_ylabel('Current (uA)')
#             ax.legend(loc='upper left', prop={'size': 6})
#             ax.set_facecolor('red')
#     except OSError:
#         print(f"Warning: Failed to read file: {file_path}")

# if __name__ == '__main__':

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-I","--Input",help ="Directory/to/data/for/IV")
#     parser.add_argument("-PS","--PowerSupply",help = "Power supply used to take IVs. (C)aen or (K)eithly")
#     args = parser.parse_args()

#     filepath = args.Input
#     powersupply = args.PowerSupply

#     IV_file = [f'ivcurve{i}.txt' for i in range(20)]

#     if powersupply == 'k':
#         plt.rcParams.update({'font.size': 8})
#         figIV, axIV= plt.subplots(2, 2, figsize=(8, 8))
#         for i in range(4):
#             plot_IV_data(filepath+ IV_file[i],i,axIV[0,0])
#             axIV[0,0].set_title('Quadrant 1')
#         for i in range(4,8):
#             plot_IV_data(filepath+ IV_file[i],i, axIV[0,1])
#             axIV[0,1].set_title('Quadrant 2')
#         for i in range(8,12):
#             plot_IV_data(filepath+ IV_file[i],i ,axIV[1,0])
#             axIV[1,0].set_title('Quadrant 3')
#         for i in range(12,16):
#             plot_IV_data(filepath+ IV_file[i],i, axIV[1,1])
#             axIV[1,1].set_title('Quadrant 4')

#         plot_IV_data(filepath+ IV_file[16],'quad 1 sum', axIV[0,0])
#         plot_IV_data(filepath+ IV_file[17],'quad 2 sum', axIV[0,1])
#         plot_IV_data(filepath+ IV_file[18],'quad 3 sum', axIV[1,0])
#         plot_IV_data(filepath+ IV_file[19],'quad 4 sum', axIV[1,1])
#         plt.tight_layout()
#         plt.show()

#     if powersupply == 'c':
#         df = pd.read_csv(filepath)
#         plt.rcParams.update({'font.size': 12})
#         figIV, axIV= plt.subplots(1, 1, figsize=(8, 6))
#         for i in range(1,5):
#             plot_IV_data(df[(df['Quadrant']==1) & (df['Tile']==i)],i,axIV)
#             axIV.set_title('Quadrants')
#         # for i in range(1,5):
#         #     plot_IV_data(df[(df['Quadrant']==2) & (df['Tile']==i)],i, axIV[0,1])
#         #     axIV[0,1].set_title('Quadrant 2')
#         # for i in range(1,5):
#         #     plot_IV_data(df[(df['Quadrant']==3) & (df['Tile']==i)],i ,axIV[1,0])
#         #     axIV[1,0].set_title('Quadrant 3')
#         # for i in range(1,5):
#         #     plot_IV_data(df[(df['Quadrant']==4) & (df['Tile']==i)],i, axIV[1,1])
#         #     axIV[1,1].set_title('Quadrant 4')

#         #plot_IV_data(df[(df['Quadrant']==1) & (df['Tile']==1234)],'quad 1 sum', axIV[0,0])
#         #plot_IV_data(df[(df['Quadrant']==2) & (df['Tile']==1234)],'quad 2 sum', axIV[0,1])
#         #plot_IV_data(df[(df['Quadrant']==3) & (df['Tile']==1234)],'quad 3 sum', axIV[1,0])
#         #plot_IV_data(df[(df['Quadrant']==4) & (df['Tile']==1234)],'quad 4 sum', axIV[1,1])
#         plt.tight_layout()
#         plt.show()

