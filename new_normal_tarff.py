import pandas as pd
import matplotlib.pyplot as plt

# Load exported Wireshark CSV
df = pd.read_csv("tcpgood.csv")

# Convert frame.time to datetime
df['frame.time'] = pd.to_datetime(df['frame.time'], errors='coerce')

# Create relative seconds from first packet
df['Time_s'] = (df['frame.time'] - df['frame.time'].min()).dt.total_seconds().astype(int)

# Throughput (includes retransmissions)
throughput = df.groupby('Time_s')['tcp.len'].sum() * 8  # bits per second

# Goodput (exclude retransmissions based on Info column)
df_good = df[~df['Info'].str.contains("TCP Retransmission", na=False)]
goodput = df_good.groupby('Time_s')['tcp.len'].sum() * 8  # bits per second

# Plot both curves
plt.figure(figsize=(10,5))
plt.plot(throughput.index, throughput.values, label="Throughput (bps)", color="red")
plt.plot(goodput.index, goodput.values, label="Goodput (bps)", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Bits per second")
plt.title("TCP Throughput vs Goodput")
plt.legend()
plt.grid(True)
plt.show()
