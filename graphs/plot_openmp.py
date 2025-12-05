import matplotlib.pyplot as plt

# Replace with your actual measured times
threads = [1, 2, 4, 8, 16]
openmp_times = [0.013090, 0.010874, 0.005653, 0.025503, 0.007007]
serial_time = 0.018528  
openmp_speedups = [serial_time/t for t in openmp_times]

# Graph 1: Threads vs Execution Time
plt.figure(figsize=(8,6))
plt.plot(threads, openmp_times, marker='o')
plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("OpenMP: Threads vs Execution Time")
plt.grid(True)
plt.show()

# Graph 2: Threads vs Speedup
serial_time = 0.018528
openmp_speedups = [serial_time / t for t in openmp_times]

plt.figure(figsize=(8,6))
plt.plot(threads, openmp_speedups, marker='o')
plt.xlabel("Threads")
plt.ylabel("Speedup")
plt.title("OpenMP: Threads vs Speedup")
plt.grid(True)
plt.show()
