import pandas as pd
import matplotlib.pyplot as plt

# Load Wireshark CSV
df = pd.read_csv("packets.csv")

# Filter ICMP packets
icmp = df[df["Protocol"] == "ICMP"]

# Separate requests and replies
requests = icmp[icmp["Info"].str.contains("Echo (ping) request", na=False, regex=False)].reset_index(drop=True)
replies = icmp[icmp["Info"].str.contains("Echo (ping) reply", na=False, regex=False)].reset_index(drop=True)

# Count totals
num_requests = len(requests)
num_replies = len(replies)

# Overall packet loss percentage
if num_requests > 0:
    packet_loss = ((num_requests - num_replies) / num_requests) * 100
    print(f"Total Requests: {num_requests}")
    print(f"Total Replies: {num_replies}")
    print(f"Overall Packet Loss (%): {packet_loss:.2f}")
else:
    print("No ICMP Echo Requests found in the CSV.")

# --- Plot packet loss trend over time ---
# Group requests by time intervals (e.g., 1 second bins)
requests["Time"] = pd.to_numeric(requests["Time"], errors="coerce")
replies["Time"] = pd.to_numeric(replies["Time"], errors="coerce")

# Define bins (1 second intervals)
time_bins = pd.interval_range(start=icmp["Time"].min(), end=icmp["Time"].max(), freq=1)

loss_percentages = []
bin_centers = []

for interval in time_bins:
    req_bin = requests[(requests["Time"] >= interval.left) & (requests["Time"] < interval.right)]
    rep_bin = replies[(replies["Time"] >= interval.left) & (replies["Time"] < interval.right)]
    if len(req_bin) > 0:
        loss = ((len(req_bin) - len(rep_bin)) / len(req_bin)) * 100
        loss_percentages.append(loss)
        bin_centers.append((interval.left + interval.right) / 2)

# Plot packet loss vs time
plt.figure(figsize=(10,6))
plt.plot(bin_centers, loss_percentages, color="red", marker="o", label="Packet Loss (%)")
plt.title("Packet Loss Over Time (High Traffic)")
plt.xlabel("Time (s)")
plt.ylabel("Packet Loss (%)")
plt.legend()
plt.grid(True)
plt.show()
