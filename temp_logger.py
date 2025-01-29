import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime

# Define file paths
file_paths = ["temperature_log_15_18_to_16_40_14112024_refilling.txt", 
              "temperature_log_16_41_14112024.txt","temperature_log_10_36_to 15_15_141124.txt","temperature_log.txt",
              "temperature_log_21_34_1611124_14_00_171124.txt","temperature_log_161124_0000_2133.txt"]

# Initialize storage for data
time_data_all = []  # Store all timestamps
temp_data_all = {0: [], 1: [], 2: [], 3: []}  # Separate lists for each channel (ignore channel 4)

# Function to read and parse a file
def process_file(file_path, time_data, temp_data):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                if "Temperature ch" in line:
                    # Split the line into timestamp and data
                    timestamp, data = line.split(" - ")
                    time = datetime.strptime(timestamp.strip(), "%Y-%m-%d %H:%M:%S,%f")
                    
                    # Extract channel and temperature
                    channel_data = data.split(":")
                    channel = int(channel_data[0].split()[2])  # Extract channel number
                    temperature = float(channel_data[1].split()[1][:-2])  # Extract temperature

                    # Append the time only if channel 0 is encountered (ensures synchronization)
                    if channel == 0:
                        time_data.append(time)

                    # Store temperature for the respective channel
                    if channel in temp_data:  # Ignore channel 4 in third file
                        temp_data[channel].append(temperature)
            except Exception as e:
                print(f"Error processing line: {line.strip()}")
                print(f"Details: {e}")

# Process each file
for file_path in file_paths:
    process_file(file_path, time_data_all, temp_data_all)

# Synchronize all data lengths
min_length = min(len(time_data_all), *[len(temps) for temps in temp_data_all.values()])
time_data_all = time_data_all[:min_length]
for channel in temp_data_all:
    temp_data_all[channel] = temp_data_all[channel][:min_length]

# Plot the data as scatter plot
# plt.figure(figsize=(15, 7))
# for channel, temps in temp_data_all.items():
#     plt.scatter(time_data_all, temps, label=f"Channel {channel}", s=2)  # s=10 sets marker size
plt.figure(figsize=(15, 7))
for channel, temps in temp_data_all.items():
    plt.scatter(time_data_all[::120], temps[::120], label=f"Channel {channel}", s=2)  # s=2 sets marker size

# Format the plot
plt.title("Temperature vs Time for Each Channel")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
# plt.ylim(-200,-100)
plt.legend()
#plt.grid(True)

# Format x-axis to display full date and time
date_formatter = DateFormatter("%Y-%m-%d %H:%M:%S")
plt.gca().xaxis.set_major_formatter(date_formatter)
plt.gcf().autofmt_xdate()  # Rotate and format x-axis labels for better readability

plt.tight_layout()
plt.show()
