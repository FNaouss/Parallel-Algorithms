#!/usr/bin/env python3
import subprocess
import os
import matplotlib.pyplot as plt
import numpy as np
import re

nr_threads_list = [2, 4, 8]


def run_and_plot(exec_name: str, start_range: int, end_range: int):
    print(f"Benchmarking: {exec_name}")

    time_serial = []
    time_parallel = []
    N_list = []

    ## SERIAL EXECUTION
    for i in range(start_range, end_range):
        N = i
        N_list.append(N)
        my_env = os.environ.copy()
        my_env["ONLY_SERIAL"] = "true"
        if "ONLY_PARALLEL" in my_env:
            del my_env["ONLY_PARALLEL"]

        result = subprocess.run([exec_name, str(N)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
        output = result.stdout.decode("utf-8")

        time_found = False
        for line in output.splitlines():
            if "serial" in line:
                times = re.findall(r"[-+]?\d*\.\d+|\d+ s", line)
                if len(times) > 1:  
                    t = str(times[1])  # elapsed_real_time
                    time_serial.append(float(t))
                    time_found = True
                    print(f"{N};{2**N};{exec_name};serial;1;{t}", flush=True)

        if not time_found:
            print(f"Warning: No valid time found for serial execution at N={N}. Adding placeholder.")
            time_serial.append(None)  
    ## PARALLEL EXECUTION
    for n_threads in nr_threads_list:
        my_env = os.environ.copy()
        my_env["OMP_NUM_THREADS"] = str(n_threads)
        my_env["ONLY_PARALLEL"] = "true"
        if "ONLY_SERIAL" in my_env:
            del my_env["ONLY_SERIAL"]

        time_parallel_with_n_threads = []
        for i in range(start_range, end_range):
            N = i
            result = subprocess.run([exec_name, str(N)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
            output = result.stdout.decode("utf-8")

            time_found = False
            for line in output.splitlines():
                if "parallel" in line:
                    times = re.findall(r"[-+]?\d*\.\d+|\d+ s", line)
                    if len(times) > 1:  
                        t = str(times[1])  # elapsed_real_time
                        time_parallel_with_n_threads.append(float(t))
                        time_found = True
                        print(f"{N};{2**N};{exec_name};parallel;{n_threads};{t}", flush=True)

            if not time_found:
                print(f"Warning: No valid time found for parallel execution at N={N}, {n_threads} threads. Adding placeholder.")
                time_parallel_with_n_threads.append(None) 

        time_parallel.append(time_parallel_with_n_threads)
    while len(time_serial) < len(N_list):
        time_serial.append(None)

    for i in range(len(time_parallel)):
        while len(time_parallel[i]) < len(N_list):
            time_parallel[i].append(None)
    plt.figure(figsize=(10, 6))
    plt.plot(N_list, time_serial, label="Serial", marker="o")

    for i in range(len(nr_threads_list)):
        time_filtered = [t if t is not None else np.nan for t in time_parallel[i]] 
        plt.plot(N_list, time_filtered, label=f"Parallel {nr_threads_list[i]} threads", marker="o")

    plt.xlabel("N (log scale)")
    plt.ylabel("Execution Time (s)")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plot_filename = f"performance_{exec_name.replace('./', '')}.png"
    plt.savefig(plot_filename)
    print(f"Saved plot to {plot_filename}")
    plt.show()


if __name__ == "__main__":
    run_and_plot("./bubble.run", 2, 16)
    run_and_plot("./mergesort.run", 10, 28)
    run_and_plot("./odd-even.run", 10, 19)
