import matplotlib.pyplot as plt
import random

latencies = [random.uniform(0.1, 1.5) for _ in range(200)]

plt.hist(latencies, bins=20)
plt.title("Latency Distribution (Response Time)")
plt.xlabel("Response Time (seconds)")
plt.ylabel("Frequency")

plt.savefig("latency.png")
