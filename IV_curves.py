import pandas as pd
import matplotlib.pyplot as plt
import os

print(os.getcwd())
# --- INPUTS ---
configuration = 'quadrant'  # 'quadrant' or 'tiles'
layer = 'Bottom'
file_path = f"../vPDU_apr-may25/cold_tests/" + layer + "/Data/12052025_IV_cold_92_75_94_65_85_" + configuration + "_1s.csv"
tile_groups = ['1', '2', '3', '4']
save = False

# --- Load and Clean Data ---
df = pd.read_csv(file_path)
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna()
df["Tile"] = df["Tile"].astype(str)

# --- vPDU QR Codes ---
vpdu_bottom = {
    0: '24073106000092002',
    1: '24073106000075002',
    2: '24092506000094002',
    3: '24092506000065002',
    4: '24092506000085002',
}

vpdu_top = {
    0: '24073106000051002',
    1: '24073106000048002',
    2: '24092506000098002',
}

# --- Plotting Functions ---
def plot_tiles(df, voltage_col, current_col, title, save_path=None):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, prefix in zip(axes.flatten(), tile_groups):
        group = df[df["Tile"].str.startswith(prefix)]
        for tile, tile_group in group.groupby("Tile"):
            ax.plot(tile_group[voltage_col], tile_group[current_col],
                    label=f"Tile {tile}", linestyle='-')
        ax.set_title(f"Quadrant {prefix}")
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (uA)")
        ax.legend(fontsize="small")
    fig.suptitle(title, fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    if save and save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

def plot_quadrant(df, voltage_col, current_col, title, save_path=None):
    plt.figure(figsize=(10, 8))
    i = 0
    for prefix in tile_groups:
        group = df[df["Tile"].str.startswith(prefix)]
        for tile, tile_group in group.groupby("Tile"):
            plt.plot(tile_group[voltage_col], tile_group[current_col],
                     label=f"Quadrant {tile_groups[i]}", linestyle='-')
            i = i + 1
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (uA)")
    plt.legend(fontsize="small")
    plt.title(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    if save and save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

# --- Plot Loop ---
vpdus = vpdu_bottom if layer == 'Bottom' else vpdu_top
for i in range(5):
    voltage_col = f"CAEN{i}_Voltage (V)"
    current_col = f"CAEN{i}_Current (uA)"
    title = f"vPDU - {vpdus[i]}"
    save_path = f"Bottom/{vpdus[i]}_tile.png" if save else None

    if configuration == 'tiles':
        plot_tiles(df, voltage_col, current_col, title, save_path)
    else:
        plot_quadrant(df, voltage_col, current_col, title, save_path)
