import pandas as pd

data = {}
data["sys_enter_sendto"] = []
data["net_dev_start_xmit"] = []
data["net_dev_xmit"] = []

with open("output.txt", "r") as file:
	file.readline()
	for line in file:
		if len(line) < 2:
			continue
		timestamp = line.split("at ")[1].split()[0]

		if line.startswith("sys_enter_sendto"):
			data["sys_enter_sendto"].append(timestamp)
		elif line.startswith("net_dev_start_xmit"):
			data["net_dev_start_xmit"].append(timestamp)
		elif line.startswith("net_dev_xmit"):
			data["net_dev_xmit"].append(timestamp)

print(f"len(1): {len(data['sys_enter_sendto'])}")
print(f"len(2): {len(data['net_dev_start_xmit'])}")
print(f"len(3): {len(data['net_dev_xmit'])}")


df = pd.DataFrame.from_dict(data)

print(df)
