import matplotlib.pyplot as plt

# Replace with your actual measured times
processes = [1, 2, 4, 8]
mpi_times = [0.016958, 0.008503, 0.006408, 0.003826]
serial_time = 0.018528 
mpi_speedups = [serial_time/t for t in mpi_times]

# Graph 1: Processes vs Execution Time
plt.figure(figsize=(8,6))
plt.plot(processes, mpi_times, marker='s')
plt.xlabel("Processes")
plt.ylabel("Execution Time (s)")
plt.title("MPI: Processes vs Execution Time")
plt.grid(True)
plt.show()

# Graph 2: Processes vs Speedup
plt.figure(figsize=(8,6))
plt.plot(processes, mpi_speedups, marker='s')
plt.xlabel("Processes")
plt.ylabel("Speedup")
plt.title("MPI: Processes vs Speedup")
plt.grid(True)
plt.show()
