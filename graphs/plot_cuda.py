#ran this on google colab
import matplotlib.pyplot as plt

configs = ["256x256 (1M)", "256x256 (5M)"]
cuda_times = [1.568, 2.868]  # in milliseconds
serial_time_ms = 18.528
cuda_speedups = [serial_time_ms / t for t in cuda_times]

# Graph 1: Config vs Execution Time
plt.figure(figsize=(8,6))
plt.plot(configs, cuda_times, marker='^')
plt.xlabel("Block x Threads Configuration")
plt.ylabel("Execution Time (ms)")
plt.title("CUDA: Config vs Execution Time")
plt.grid(True)
plt.show()

# Graph 2: Config vs Speedup
plt.figure(figsize=(8,6))
plt.plot(configs, cuda_speedups, marker='^')
plt.xlabel("Block x Threads Configuration")
plt.ylabel("Speedup")
plt.title("CUDA: Config vs Speedup")
plt.grid(True)
plt.show()
