import pandas as pd
import matplotlib.pyplot as plt
import re

# Load your packets.csv
df = pd.read_csv("packets.csv")

# Filter ICMP packets
icmp = df[df["Protocol"] == "ICMP"]

# Separate requests and replies (literal string match, not regex)
requests = icmp[icmp["Info"].str.contains("Echo (ping) request", na=False, regex=False)].reset_index(drop=True)
replies = icmp[icmp["Info"].str.contains("Echo (ping) reply", na=False, regex=False)].reset_index(drop=True)

latencies = []

# Match by sequence number
for i, req in requests.iterrows():
    match = re.search(r"seq=(\d+/\d+)", req["Info"])
    if match:
        seq = match.group(1)
        rep = replies[replies["Info"].str.contains(f"seq={seq}", na=False, regex=False)]
        if not rep.empty:
            req_time = float(req["Time"])
            rep_time = float(rep.iloc[0]["Time"])
            latency = (rep_time - req_time) * 1000  # ms
            latencies.append(latency)

# Compute jitter only if we have enough latency values
jitter = []
if len(latencies) > 1:
    jitter = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]

# Plot latency
plt.figure(figsize=(10,6))
plt.plot(latencies, label="Latency (ms)", color="blue")
plt.title("ICMP Latency")
plt.xlabel("Packet Index")
plt.ylabel("Milliseconds")
plt.legend()
plt.grid(True)
plt.show()

# Plot jitter
if jitter:
    plt.figure(figsize=(10,6))
    plt.plot(range(1, len(latencies)), jitter, label="Jitter (ms)", color="orange")
    plt.title("ICMP Jitter")
plt.xlabel("Packet Index")
plt.ylabel("Milliseconds")
plt.legend()
plt.grid(True)
plt.show()

# Print summary stats
if latencies:
    print("Average Latency (ms):", sum(latencies)/len(latencies))
    print("Max Latency (ms):", max(latencies))
if jitter:
    print("Average Jitter (ms):", sum(jitter)/len(jitter))
