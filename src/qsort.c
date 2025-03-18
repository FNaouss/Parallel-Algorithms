#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#include "sorting.h"

int compare(const void *a, const void *b) {
    return (*(uint64_t *)a - *(uint64_t *)b);
}

void sequential_quick_sort(uint64_t *T, uint64_t size) {
    qsort(T, size, sizeof(uint64_t), compare);
}
void parallel_quick_sort(uint64_t *T, uint64_t size) {
    if (size <= 1) return;
    uint64_t pivot = T[size / 2];
    uint64_t i = 0, j = size - 1;
    while (i <= j) {
        while (T[i] < pivot) i++;
        while (T[j] > pivot) j--;
        if (i <= j) {
            uint64_t temp = T[i];
            T[i] = T[j];
            T[j] = temp;
            i++;
            j--;
        }
    }

    #pragma omp parallel sections
    {
        #pragma omp section
        parallel_quick_sort(T, j + 1);
        
        #pragma omp section
        parallel_quick_sort(T + i, size - i);
    }
}



int main(int argc, char **argv) {
    struct cpu_stats *stats = cpu_stats_init();
    unsigned int exp;

    if (argc != 2) {
        fprintf(stderr, "Usage: quicksort.run N \n");
        exit(-1);
    }

    uint64_t N = 1 << atoi(argv[1]);
    uint64_t *X = (uint64_t *)malloc(N * sizeof(uint64_t));

    printf("--> Sorting an array of size %lu\n", N);

    for (exp = 0; exp < NB_EXPERIMENTS; exp++) {
        init_array_random(X, N);
        cpu_stats_begin(stats);
        sequential_quick_sort(X, N);
        experiments[exp] = cpu_stats_end(stats);

        if (!is_sorted(X, N)) {
            fprintf(stderr, "ERROR: Sequential quicksort failed\n");
            exit(-1);
        }
    }

    println_cpu_stats_report("quick sort serial", average_report(experiments, NB_EXPERIMENTS));
    for (exp = 0; exp < NB_EXPERIMENTS; exp++) {
        init_array_random(X, N);
        cpu_stats_begin(stats);
        parallel_quick_sort(X, N);
        experiments[exp] = cpu_stats_end(stats);

        if (!is_sorted(X, N)) {
            fprintf(stderr, "ERROR: Parallel quicksort failed\n");
            exit(-1);
        }
    }

    println_cpu_stats_report("quick sort parallel", average_report(experiments, NB_EXPERIMENTS));
    uint64_t *Y = (uint64_t *)malloc(N * sizeof(uint64_t));
    uint64_t *Z = (uint64_t *)malloc(N * sizeof(uint64_t));
    init_array_random(Y, N);
    memcpy(Z, Y, N * sizeof(uint64_t));
    sequential_quick_sort(Y, N);
    parallel_quick_sort(Z, N);

    if (!are_vector_equals(Y, Z, N)) {
        fprintf(stderr, "ERROR: Sequential and parallel quicksort results differ\n");
        exit(-1);
    }

    free(X);
    free(Y);
    free(Z);
}
