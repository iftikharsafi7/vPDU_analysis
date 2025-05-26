import pandas as pd
import matplotlib.pyplot as plt
import os
import json




# --- Functions ---
def load_setup(file):
    with open(file, 'r') as f:
        data = json.load(f)

        return {int(k): v for k, v in data.items()}
    
def load_data(file, n_vpdus, threshold = 35, exception = False ):
    # --- Load and Clean Data ---
    df = pd.read_csv(file)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()
    df["Tile"] = df["Tile"].astype(str)
    try:
        for i in range(n_vpdus):
            df = df[(df[f'CAEN{i}_Voltage (V)'] >= threshold)]
    except KeyError:
        for i in range(1, n_vpdus):
            df = df[(df[f'CAEN{i}_Voltage (V)'] >= threshold)]
    return df
    

def plot_tiles(df, voltage_col, current_col, title, tile_groups = ['1', '2', '3', '4'], 
               save = False,  save_path=None):
    
    tile_groups = ['1', '2', '3', '4']
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    for ax, prefix in zip(axes.flatten(), tile_groups):
        group = df[df["Tile"].str.startswith(prefix)]
        for tile, tile_group in group.groupby("Tile"):
            ax.plot(tile_group[voltage_col], tile_group[current_col],
                    label=f"Tile {tile}", linestyle='-')
        ax.set_title(f"Quadrant {prefix}")
        #ax.xlim([35,70])
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (uA)")
        ax.legend(fontsize="small")
    fig.suptitle(title, fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    if save and save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

def plot_quadrant(df, voltage_col, current_col, title, tile_groups = ['1', '2', '3', '4'], 
               save = False,  save_path=None):
    plt.figure(figsize=(8, 6))
    i = 0
    for prefix in tile_groups:
        group = df[df["Tile"].str.startswith(prefix)]
        for tile, tile_group in group.groupby("Tile"):
            plt.plot(tile_group[voltage_col], tile_group[current_col],
                     label=f"Quadrant {tile_groups[i]}", linestyle='-')
            i = i + 1
    plt.xlabel("Voltage (V)")
    #plt.xlim([35,70])
    plt.ylabel("Current (uA)")
    plt.legend(fontsize="small")
    plt.title(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    if save and save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

if __name__ == "__main__":
    print(os.getcwd())
    # --- INPUTS ---
    configuration = 'quadrant'  # 'quadrant' or 'tiles'
    layer = 'Bottom'
    file_path = '../vPDU_apr-may25/Batch_2/Data/IV/IV_warm_76_103_65_51_quadrants_23052025_3s.csv' #f"../vPDU_apr-may25/cold_tests/" + layer + "/Data/12052025_IV_cold_92_75_94_65_85_" + configuration + "_1s.csv"
    tile_groups = ['1', '2', '3', '4']
    save = False

    # --- Load and Clean Data ---
    df = pd.read_csv(file_path)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()
    df["Tile"] = df["Tile"].astype(str)
    df = df[(df['CAEN1_Voltage (V)'] >= 35) & (df['CAEN2_Voltage (V)'] >= 35) & (df['CAEN3_Voltage (V)'] >= 35) & (df['CAEN4_Voltage (V)'] >= 35)]
    
    # --- vPDU QR Codes ---
    vpdu_bottom = {
        1: '24092506000076002',
        2: '24092506000103002',
        3: '24092506000065002',
        4: '24073106000051002'
    }

    vpdu_top = {
        0: '24092506000098002',
        1: '24092506000057002',
        2: '24092506000083002',
    }


    # --- Plot Loop ---
    vpdus = vpdu_bottom if layer == 'Bottom' else vpdu_top
    for i in range(1,len(vpdus)+1):
        voltage_col = f"CAEN{i}_Voltage (V)"
        current_col = f"CAEN{i}_Current (uA)"
        title = f"vPDU - {vpdus[i]}"
        save_path = f"../vPDU_apr-may25/warm_tests/Plots/Test2/Bottom/vpdus{i}_quadrant.png" if save else None
    
        if configuration == 'tiles':
            plot_tiles(df, voltage_col, current_col, title, save_path)
        else:
            plot_quadrant(df, voltage_col, current_col, title, save_path)
