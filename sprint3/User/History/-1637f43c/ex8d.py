import matplotlib.pyplot as plt
import pandas as pd

import pandas as pd

data = {}
data["sys_enter_sendto_timestamps"] = []
data["net_dev_xmit_timestamps"] = []
data["latency"] = []

def get_data_frame(): 
    with open("output.txt", "r") as file:
    	file.readline()
    	for line in file:
    		if len(line) < 2:
    			continue
    		timestamp = line.split(": ")[1].split()[0]
    		key = line.split("[")[1].split("]")[0]  
    		# print(key)
    		# print(timestamp)
    		if line.startswith("@sendto"):
    			data["sys_enter_sendto_timestamps"].append([key, timestamp])
    		elif line.startswith("@xmit"):
    			data["net_dev_xmit_timestamps"].append([key, timestamp])

    for i in range(min(len(data["sys_enter_sendto_timestamps"]), len(data["net_dev_xmit_timestamps"]))):
        sendto_ts = int(data["sys_enter_sendto_timestamps"][i][1])
        xmit_ts = int(data["net_dev_xmit_timestamps"][i][1])
        latency = xmit_ts - sendto_ts
        data["latency"].append(latency)
   
    
    print(f"len(1): {len(data['sys_enter_sendto_timestamps'])}")
    print(f"len(2): {len(data['net_dev_xmit_timestamps'])}")
    
    
    df = pd.DataFrame.from_dict(data)
    df.to_csv("data.csv", index="false")
    print(df)
    return df


def plot_timeline(data):
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    # Plot sys_enter_sendto_timestamps
    axes[0].hlines(1, min(data['sys_enter_sendto_timestamps'].apply(lambda x: x[1])), 
                   max(data['sys_enter_sendto_timestamps'].apply(lambda x: x[1])), colors='black', linewidth=1.5)
    axes[0].scatter(data['sys_enter_sendto_timestamps'].apply(lambda x: x[1]), [1] * len(data), color='blue', label='sys_enter_sendto')
    axes[0].set_ylabel("sys_enter_sendto")
    axes[0].legend()
    
    # Plot net_dev_xmit_timestamps
    axes[1].hlines(1, min(data['net_dev_xmit_timestamps'].apply(lambda x: x[1])), 
                   max(data['net_dev_xmit_timestamps'].apply(lambda x: x[1])), colors='black', linewidth=1.5)
    axes[1].scatter(data['net_dev_xmit_timestamps'].apply(lambda x: x[1]), [1] * len(data), color='red', label='net_dev_xmit')
    axes[1].set_ylabel("net_dev_xmit")
    axes[1].legend()
    
    # Adjust plot labels
    axes[1].set_xlabel("Timestamp (ns)")
    plt.suptitle("Event Timestamps")
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")
    
    # Save the plot to a JPG file
    plt.savefig("timeline_plot.jpg", format="jpg", dpi=300, bbox_inches='tight')
    
    # Save the plot to a JPG file
    plt.savefig("timeline_plot.jpg", format="jpg", dpi=300)
    
    # plt.show()

def plot_latency(df):
    """
    Plots latency (y-axis) against packet ID (x-axis).

    Args:
        df (pd.DataFrame): DataFrame containing the latency data.
    """
    if "latency" not in df.columns:
        raise ValueError("The DataFrame does not contain a 'latency' column.")

    # Extract packet IDs and latency values
    packet_ids = range(len(df["latency"]))
    latency_values = df["latency"]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(packet_ids, latency_values, marker="o", linestyle="-", color="b", label="Latency")
    plt.xlabel("Packet ID")
    plt.ylabel("Latency (ns)")
    plt.title("Latency vs Packet ID")
    plt.grid(True)
    plt.legend()
    plt.savefig("latency_plot.jpg", format="jpg", dpi=300)
    # plt.show()

# Call Dataframe function
data = get_data_frame()
# Call the function to plot
plot_timeline(data)
plot_latency(data)