import pandas as pd
import matplotlib.pyplot as plt

# Load exported ICMPv6 CSV
df = pd.read_csv("icmpv6.csv")

# Use raw strings for regex to avoid escape warnings
requests = df[df['Info'].str.contains(r"Echo \(ping\) request", na=False)]
replies = df[df['Info'].str.contains(r"Echo \(ping\) reply", na=False)]

# Match requests and replies by sequence number
rtt_list = []
for _, req in requests.iterrows():
    seq = int(req['Info'].split("seq=")[1].split(",")[0])
    reply = replies[replies['Info'].str.contains(f"seq={seq}", na=False)]
    if not reply.empty:
        rtt = float(reply.iloc[0]['Time']) - float(req['Time'])
        rtt_list.append((seq, rtt * 1000))  # convert to ms

# Convert to DataFrame
rtt_df = pd.DataFrame(rtt_list, columns=['Seq', 'RTT_ms'])

# Compute jitter (difference between successive RTTs)
rtt_df['Jitter_ms'] = rtt_df['RTT_ms'].diff().abs()

# Plot RTT
plt.figure(figsize=(10,5))
plt.plot(rtt_df['Seq'], rtt_df['RTT_ms'], marker='o', label='RTT (ms)')
plt.xlabel("Sequence Number")
plt.ylabel("RTT (ms)")
plt.title("ICMPv6 Latency (RTT)")
plt.legend()
plt.grid(True)
plt.show()

# Plot Jitter
plt.figure(figsize=(10,5))
plt.plot(rtt_df['Seq'], rtt_df['Jitter_ms'], marker='o', color='orange', label='Jitter (ms)')
plt.xlabel("Sequence Number")
plt.ylabel("Jitter (ms)")
plt.title("ICMPv6 Jitter")
plt.legend()
plt.grid(True)
plt.show()
