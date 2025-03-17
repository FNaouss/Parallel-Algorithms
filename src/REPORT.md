# **Parallel sorting algorithms - Lab 2 report**

## **Participants**
- Hatim RIDAOUI
- Nacer-Eddine FARDOUS

## **Overview**
This project implements and analyzes different sorting algorithms using **OpenMP** for parallelization. We compare their performance and propose optimizations where applicable.

## **1. Bubble sort (6 points)**
### **What we did**
- Implemented **sequential bubble sort**.
- Implemented **parallel bubble sort** using OpenMP.
- Verified correctness by comparing sequential and parallel results.

### **Performance**
| Threads | CPU cycles | Elapsed CPU time (s) | Elapsed real time (s) |
|---------|------------|----------------------|-----------------------|
| 16      | -         | -                    | -                     |

### **Limitations**
- **High overhead**: bubble sort is inherently inefficient.
- **Parallel speedup is limited** due to heavy **synchronization**.

---

## **2. Merge sort with tasks (5 points)**
### **What we did**
- Implemented **sequential merge sort**.
- Implemented **parallel merge sort** using OpenMP tasks.
- Added **performance testing** with different thread counts (2, 4, 8, 16).
- **Identified performance bottlenecks**:
  - **Too many tasks for small inputs**, leading to **task creation overhead**.
  - **Merge step remains sequential**, limiting speedup.
- Proposed and implemented an **optimized version**:
  - **Uses a dynamic cutoff** to avoid excessive task creation.
  - **Performance tested it**, but observed **limited improvement**.

### **Performance**
| Threads | Input size | CPU cycles | Elapsed CPU time (s) | Elapsed real time (s) |
|---------|------------|------------|----------------------|-----------------------|
| 2       | 32,768     | 2,612,857  | 0.001971             | 0.001079              |
| 8       | 32,768     | 6,392,529  | 0.028562             | 0.003987              |
| 16      | 32,768     | 1,237,249  | 0.005482             | 0.002819              |

| Threads | Input size | CPU cycles | Elapsed CPU time (s) | Elapsed real time (s) |
|---------|------------|------------|----------------------|-----------------------|
| 4       | 1,048,576  | 69,515,108 | 0.152582             | 0.058705              |

### **Limitations**
- **Parallel merge sort is still slower than expected**.
- **Scaling beyond 4-8 threads does not give significant speedup**.

---

## **3. Odd-even sort (4 points)**
### **What we missed**
- This part **was not implemented** yet.
- The report needs an **explanation of why odd-even sort is better suited for parallelization**.

---

## **4. Performance analysis (5 points)**
### **What we did**
- **Ran experiments** on sorting algorithms with different thread counts and input sizes.
- **Collected CPU cycles, elapsed time, and real-time execution data**.
- **Identified key findings**:
  - **Bubble sort does not scale well**.
  - **Parallel merge sort has overhead issues**.
  - **Thread count above 8 does not improve performance**.
- Used `plot_times.py` (provided script) to generate graphs.

### **Limitations**
- Further **optimizations in the merging phase** could improve merge sort performance.
- We **still need a clear explanation of performance scaling** in the report.

---

## **5. Proposed optimization (4c - merge sort)**
### **Implemented improvement**
- **Added an adaptive threshold** to avoid unnecessary task creation.
- Used **`omp_get_max_threads()`** to determine thread count dynamically.

### **Results**
- **Improvement was marginal**, as the merge phase remains sequential.
- **Task overhead still affects performance for large inputs**.

