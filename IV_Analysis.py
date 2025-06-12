import numpy as np
import sys
sys.path.append("../")
sys.path.append("../vPDU_reco-ana/veto_passport/AnalysisTools")
import CharacterisationTools as analysis
import IVAnalysis as IVAnalysis
import matplotlib.pyplot as plt
import os


def plot_group(file_indices, title, Vlim = [15, 80], save = False, save_path = None):
    
    IV = IVAnalysis.IVAnalysis()
    Vbd_Cold = [None] * 20
    Vbd_cold_err = [None] * 20

    plt.figure(figsize=[10, 8])
    for idx in file_indices:
        try:
            Vbd, Vbd_err = IV.calc_Vbd(file[idx], Vstart=Vlim[0], Vstop=Vlim[1], plot_opt=True)
            IV.plot_tileIV(file[idx], label=f"Q{idx+1}, {Vbd:.2f} V")
            line = plt.gca().lines[-1]
            plt.axvline(Vbd, color=line.get_color(), linestyle=':', linewidth=3)
            print(f"✅ Q{idx+1}: Vbd = {Vbd:.2f} V ± {Vbd_err:.2f}")
        except Exception as e:
            print(f"❌ Fitting failed for ColdTileIV{idx+1}: {e}")
            continue
    plt.xlabel("Voltage [V]")
    plt.ylabel("Current [A]")
    plt.title(title)
    #plt.xlim(45, 64)
    plt.ylim(2.3, 140)
    #plt.legend()
    if save == True:
        plt.savefig(save_path)
    plt.show()
    

plt.rcParams.update({'font.size': 18}) 
plt.rcParams.update({'lines.linewidth': 3}) 
plt.rcParams.update({'xtick.direction': 'in'}) 
plt.rcParams.update({'ytick.direction': 'in'})


if __name__ == '__main__':
    #base_path = "/Users/astrocent/test_pdu/IV_data/IV_bottom_files/IVs/Cold/Top/IV_cold_51_48_98_quadrant_3s_v2"
    base_path = "/home/diego/Desktop/Astrocent/vPDUs/vPDU_apr-may25/Batch_2/warm_tests/Data/IV/splitted/"
    #base_path ="/Users/astrocent/test_pdu/IV_data/IV_bottom_files/IVs/cold/Bottom/12052025_IV_cold_92_75_94_65_85_quadrant_1s"
    #base_path ="/Users/astrocent/test_pdu/IV_data/IV_bottom_files/IVs/Cold/Bottom/vPDU-65"
    file = [os.path.join(base_path, f"IV_q{i}.txt") for i in range(12)]
    
    IV = IVAnalysis.IVAnalysis()
    Vbd_Cold = [None] * 4
    Vbd_cold_err = [None] * 4
    
    
    
    
    
    # Plot files 0 to 3 in one figure
    plot_group([0,1,2,3], title="vPDU-24092506000098002")
    plot_group([4,5,6,7], title="vPDU-24092506000057002")
    plot_group([8,9,10,11], title="vPDU-24092506000083002")