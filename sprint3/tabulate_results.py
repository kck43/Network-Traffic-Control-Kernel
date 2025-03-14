import pandas as pd

data = {}
data["sys_enter_sendto_timestamps"] = []
data["net_dev_xmit_timestamps"] = []

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



print(f"len(1): {len(data['sys_enter_sendto_timestamps'])}")
print(f"len(2): {len(data['net_dev_xmit_timestamps'])}")


df = pd.DataFrame.from_dict(data)

print(df.head())
