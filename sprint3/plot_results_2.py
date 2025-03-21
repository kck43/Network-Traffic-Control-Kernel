import matplotlib.pyplot as plt
import pandas as pd

import pandas as pd

data = {}
data["sys_enter_sendto_timestamps"] = []
data["net_dev_xmit_timestamps"] = []
data["net_dev_start_xmit_timestamps"] = []
data["sendto_to_start_latency"] = []
data["start_to_xmit_latency"] = []
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
                data["sys_enter_sendto_timestamps"].append([key, int(timestamp)])
            elif line.startswith("@xmit"):
                data["net_dev_xmit_timestamps"].append([key, int(timestamp)])
            elif line.startswith("@start_xmit"):
                data["net_dev_start_xmit_timestamps"].append([key, int(timestamp)])

    for i in range(min(len(data["sys_enter_sendto_timestamps"]), len(data["net_dev_xmit_timestamps"]))):
        sendto_ts = int(data["sys_enter_sendto_timestamps"][i][1])
        xmit_ts = int(data["net_dev_xmit_timestamps"][i][1])
        start_xmit_ts = int(data["net_dev_start_xmit_timestamps"][i][1])
        latency = xmit_ts - sendto_ts
        sendto_to_start_latency = start_xmit_ts - sendto_ts
        start_to_xmit_latency = xmit_ts - start_xmit_ts
        data["latency"].append(latency)
        data["sendto_to_start_latency"].append(sendto_to_start_latency)
        data["start_to_xmit_latency"].append(start_to_xmit_latency)

   
    
    print(f"len(1): {len(data['sys_enter_sendto_timestamps'])}")
    print(f"len(2): {len(data['net_dev_xmit_timestamps'])}")
    
    
    df = pd.DataFrame.from_dict(data)
    df.to_csv("more_tracepoints_data.csv", index="false")
    print(df)
    return df



# def plot_timeline(data):
#     fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
#     # Extract timestamps
#     sendto_timestamps = data['sys_enter_sendto_timestamps'].apply(lambda x: x[1])
#     xmit_timestamps = data['net_dev_xmit_timestamps'].apply(lambda x: x[1])
    
#     # Normalize timestamps by subtracting the first sendto timestamp
#     start_time = sendto_timestamps.min()
#     sendto_timestamps = sendto_timestamps - start_time
#     xmit_timestamps = xmit_timestamps - start_time

#     # Compute global min and max after normalization
#     global_min = 0  # First sendto timestamp is now at time 0
#     global_max = max(sendto_timestamps.max(), xmit_timestamps.max())

#     # Plot sys_enter_sendto_timestamps
#     axes[0].hlines(1, global_min, global_max, colors='black', linewidth=1.5)
#     axes[0].scatter(sendto_timestamps, [1] * len(data), color='blue', label='sys_enter_sendto')
#     axes[0].set_ylabel("sys_enter_sendto")
#     axes[0].legend()
    
#     # Plot net_dev_xmit_timestamps
#     axes[1].hlines(1, global_min, global_max, colors='black', linewidth=1.5)
#     axes[1].scatter(xmit_timestamps, [1] * len(data), color='red', label='net_dev_xmit')
#     axes[1].set_ylabel("net_dev_xmit")
#     axes[1].legend()
    
#     # Adjust plot labels
#     axes[1].set_xlabel("Time since first sendto event (ns)")
#     plt.suptitle("Event Timestamps (Normalized)")

#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45, ha="right")
    
#     # Save the plot
#     plt.savefig("timeline_plot.jpg", format="jpg", dpi=300, bbox_inches='tight')

#     # plt.show()  # Show the plot



def plot_timeline(data):
    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    
    # Extract timestamps (original, unnormalized)
    sendto_timestamps = data['sys_enter_sendto_timestamps'].apply(lambda x: x[1])
    xmit_timestamps = data['net_dev_xmit_timestamps'].apply(lambda x: x[1])
    start_timestamps = data['net_dev_start_xmit_timestamps'].apply(lambda x: x[1])

    # Store absolute timestamps before normalization
    absolute_timestamps = sorted(set(sendto_timestamps).union(set(xmit_timestamps)))

    # Normalize timestamps by subtracting the first sendto timestamp
    start_time = sendto_timestamps.min()
    sendto_timestamps = sendto_timestamps - start_time
    xmit_timestamps = xmit_timestamps - start_time
    start_timestamps = start_timestamps - start_time

    # Compute global min and max after normalization
    global_min = 0  # First sendto timestamp is now at time 0
    global_max = max(sendto_timestamps.max(), xmit_timestamps.max())

    # Plot sys_enter_sendto_timestamps
    axes[0].hlines(1, global_min, global_max, colors='black', linewidth=1.5)
    axes[0].scatter(sendto_timestamps, [1] * len(data), color='blue', label='sys_enter_sendto')
    axes[0].set_ylabel("sys_enter_sendto")
    axes[0].legend()

    axes[1].hlines(1, global_min, global_max, colors='black', linewidth=1.5)
    axes[1].scatter(start_timestamps, [1] * len(data), color='blue', label='net_dev_start_xmit')
    axes[1].set_ylabel("net_dev_start_xmit")
    axes[1].legend()
    
    # Plot net_dev_xmit_timestamps
    axes[2].hlines(1, global_min, global_max, colors='black', linewidth=1.5)
    axes[2].scatter(xmit_timestamps, [1] * len(data), color='red', label='net_dev_xmit')
    axes[2].set_ylabel("net_dev_xmit")
    axes[2].legend()
    
    # Adjust plot labels
    axes[1].set_xlabel("Time since first sendto event (ns)")
    plt.suptitle("Event Timestamps (Normalized)")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Set custom x-axis labels with absolute timestamps
    tick_positions = plt.xticks()[0]  # Get default tick positions
    absolute_labels = [str(int(start_time + tick)) for tick in tick_positions]
    axes[1].set_xticklabels(absolute_labels)  # Set the labels on the second (bottom) subplot

    # Save the plot
    plt.savefig("timeline_plot.jpg", format="jpg", dpi=300, bbox_inches='tight')

    # plt.show()  # Show the plot



def plot_latency(df):
    """
    Plots multiple latency values against packet ID.

    Args:
        df (pd.DataFrame): DataFrame containing the latency data.
    """
    required_columns = ["latency", "sendto_to_start_latency", "start_to_xmit_latency"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The DataFrame does not contain a '{col}' column.")

    # Extract packet IDs
    packet_ids = range(len(df))

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(packet_ids, df["latency"], marker="o", linestyle="-", color="b", label="Total Latency")
    plt.plot(packet_ids, df["sendto_to_start_latency"], marker="s", linestyle="--", color="r", label="Sendto to Start Latency")
    plt.plot(packet_ids, df["start_to_xmit_latency"], marker="^", linestyle="-.", color="g", label="Start to Xmit Latency")
    
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