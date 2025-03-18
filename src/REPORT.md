# Parallel sorting algorithms - Lab 2 report

## Participants
- Hatim RIDAOUI
- Nacer-Eddine FARDOUS

## Overview
This project implements and analyzes different sorting algorithms using OpenMP for parallelization. We compare their performance and propose optimizations where applicable.

## 1. Bubble sort
### What we did
- Implemented sequential and parallel bubble sort using OpenMP.
- Verified correctness by comparing sequential and parallel results.

### Performance
(See plot)

### Limitations
- High overhead due to frequent swaps and sequential dependency.
- Parallelization has limited speedup because of heavy synchronization.

---

## 2. Merge sort with tasks
### What we did
- Implemented sequential and parallel merge sort using OpenMP tasks.
- Analyzed performance for different thread counts (2, 4, 8, 16).
- Added a dynamic cutoff to reduce task creation overhead.

### Performance comparison with bubble sort
- Merge sort is more efficient than bubble sort, especially for large inputs.
- The parallel version scales better but still has overhead due to the merge phase.
- Speedup is limited beyond 4-8 threads due to sequential merging.

### Performance
| Threads | Input size | Elapsed real time (s) |
|---------|------------|-----------------------|
| 2       | 32,768     | 0.001079              |
| 8       | 32,768     | 0.003987              |
| 16      | 32,768     | 0.002819              |

### Limitations
- Parallel merge sort has overhead from excessive task creation.
- The merge step remains sequential, limiting overall speedup.

---

## 3. Odd-even sort
### What we did
- Implemented sequential and parallel odd-even sort using OpenMP.
- Used OpenMP parallel loops to swap elements.
- Verified correctness by comparing sequential and parallel results.

### Performance
- The parallel version has better load balancing than bubble sort.
- Performance depends on the number of iterations required to converge.

### Limitations
- Odd-even sort is more suited for parallelization than bubble sort but still inefficient for large inputs.
- Synchronization overhead impacts scalability.

---

## Quick sort  

### What we did  
We implemented sequential quick sort using the qsort function from the C standard library. We then implemented a parallel version using OpenMP, applying parallel task creation to improve performance. The parallel quick sort was designed to divide the array into partitions and sort them concurrently, leveraging multiple threads.  

### Performance  
We compared quick sort with merge sort to analyze performance differences. Quick sort generally performed well for large input sizes but showed some inconsistencies due to its partitioning strategy. While quick sort benefited from parallel execution, merge sort demonstrated more stable performance scaling, especially when increasing the number of threads.  


## 4. Performance analysis
### What we did
- Conducted experiments with different sorting algorithms and thread counts.
- Measured CPU cycles, elapsed time, and real-time execution data.
- Used `plot_times.py` to generate performance graphs.

### Key findings
- Bubble sort does not scale well.
- Merge sort benefits from parallelization but has limitations in merging.
- Odd-even sort is more efficient than bubble sort but remains suboptimal.
- Performance gain plateaus beyond 8 threads due to hardware limitations.

---

## 5. Performance graph analysis
The performance graph below shows execution time for serial vs. parallel sorting algorithms as input size increases.

### Observations
- For small inputs, parallel versions are slower due to thread overhead.
- Merge sort outperforms bubble and odd-even sort, particularly for large inputs.
- The speedup plateaus beyond 8 threads due to memory and synchronization overhead.

---

## 6. CPU hardware information
### System specifications
| Specification         | Value                              |
|-----------------------|----------------------------------|
| CPU Model            | Intel Core i7-7700HQ @ 2.80GHz  |
| Architecture         | x86_64 (64-bit)                  |
| Cores               | 4 (8 threads with HyperThreading) |
| L1 Cache            | 128 KB per core                   |
| L2 Cache            | 1 MB per core                     |
| L3 Cache            | 6 MB shared                       |
| Max frequency       | 2.80 GHz                          |
| Min frequency       | 800 MHz                           |
| Virtualization      | VT-x (Enabled)                    |

### Implications for performance
- The experiments used 2, 4, and 8 threads to test parallel performance.
- Merge sort was bottlenecked by sequential merging and memory bandwidth.
- HyperThreading did not significantly improve sorting performance due to memory-bound operations.

### Plot analysis

The performance plots compare the execution time of serial and parallel sorting implementations for different input sizes. Each graph shows the execution time on a logarithmic scale as the input size increases.

- **Bubble sort**: The parallel versions show little to no improvement over the serial implementation. This is due to the high synchronization cost and the inherently sequential nature of the algorithm. The overhead of parallelism outweighs the benefits for smaller inputs.

- **Merge sort**: The parallel implementation performs significantly better than the serial one for larger input sizes. However, beyond a certain number of threads, the speedup stagnates. This is mainly due to the sequential merge step, which becomes the dominant factor in execution time.

- **Odd-even sort**: The parallel implementation improves performance slightly compared to the serial version, but not as much as expected. The alternating nature of swaps introduces dependencies between iterations, limiting parallel efficiency. The results show that scalability is limited beyond a few threads.

Overall, the results highlight that parallelism benefits sorting algorithms with well-defined independent tasks, such as merge sort, whereas algorithms with frequent synchronization, like bubble sort and odd-even sort, suffer from parallel overhead.

