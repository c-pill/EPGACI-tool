#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void print_individual(int * pixels, size_t size) {
    for (int i = 0; i < size*3; i+=3) {
        printf("[");
        for (int k = 0; k < 3; k++) printf("%d ", pixels[i+k]);
        printf("],\n");
    }
}

float evaluate_fitness(int * ind_pixels, int * orig_pixels, double goal, size_t size) {
    float pixels_similar = 0;
    for (int i = 0; i < size*3; i+=3) {
        bool similar = true;
        for (int p = 0; p < 3 && similar; p++) {
            if (ind_pixels[i+p] != orig_pixels[i+p]) similar = false;
        }
        if (similar) pixels_similar++;
    }
    float percent_similar = (pixels_similar / size) * 100;
    float fitness = fabs(percent_similar - goal);
    return fitness;
}

// random int generator used because c rand() does not generate large numbers
int xorshift32(int seed) {
    int x = seed;
    x ^= (x << 13);
    x ^= (x >> 17);
    x ^= (x << 5);
    return abs(x);
}

int* mass_swap(int * pixels, int seed, size_t size) {
    int ** swapped_pixels = (int**) malloc(size * sizeof(int*));
    for (int i = 0, p = 0; i < size*3; i+=3, p++) {
        swapped_pixels[p] = (int*) malloc(3 * sizeof(int));
        for (int k = 0; k < 3; k++) swapped_pixels[p][k] = pixels[i+k];
    }
    
    int num_swaps = xorshift32(seed) % size;
    int reuse_seed = xorshift32(num_swaps) % size;

    for (int i = 0; i < num_swaps; i++) {
        reuse_seed = xorshift32(reuse_seed | rand());
        int pos1 = reuse_seed % size;
        reuse_seed = xorshift32(reuse_seed | rand());
        int pos2 = reuse_seed % size;

        int * tmp = swapped_pixels[pos1];
        swapped_pixels[pos1] = swapped_pixels[pos2];
        swapped_pixels[pos2] = tmp;
    }

    int * flattened = (int*) malloc(size*3*sizeof(int));
    for (int i = 0, j = 0; j < size; j++) {
        for (int p = 0; p < 3; i++, p++)
            flattened[i] = swapped_pixels[j][p];
        free(swapped_pixels[j]);
    }
    free(swapped_pixels);

    return flattened;
}

int* smart_swap(int * pixels, int seed, int max_swap, size_t size) {
    int ** swapped_pixels = (int**) malloc(size * sizeof(int*));
    for (int i = 0, p = 0; i < size*3; i+=3, p++) {
        swapped_pixels[p] = (int*) malloc(3 * sizeof(int));
        for (int k = 0; k < 3; k++) swapped_pixels[p][k] = pixels[i+k];
    }
    
    int num_swaps = xorshift32(seed) % max_swap;
    int reuse_seed = xorshift32(num_swaps) % size;

    for (int i = 0; i < num_swaps; i++) {
        reuse_seed = xorshift32(reuse_seed | rand());
        int pos1 = reuse_seed % size;
        reuse_seed = xorshift32(reuse_seed | rand());
        int pos2 = reuse_seed % size;

        int * tmp = swapped_pixels[pos1];
        swapped_pixels[pos1] = swapped_pixels[pos2];
        swapped_pixels[pos2] = tmp;
    }

    int * flattened = (int*) malloc(size*3*sizeof(int));
    for (int i = 0, j = 0; j < size; j++) {
        for (int p = 0; p < 3; i++, p++)
            flattened[i] = swapped_pixels[j][p];
        free(swapped_pixels[j]);
    }
    free(swapped_pixels);

    return flattened;
}

// returns position of tournament winner
int tournament_select(float * fitness, int opps, size_t size) {
    int winner = rand() % size;
    for (int k = 0; k < opps-1; k++) {
        int opp = rand() % size;
        if (fitness[winner] < fitness[opp])
            winner = rand() % 11 <= 8 ? winner : opp;
        else if (fitness[winner] == fitness[opp])
            winner = rand() % 2 == 0 ? winner : opp;
        else
            winner = rand() % 11 <= 2 ? winner : opp;
    } 
    return winner;
}

void free_pixels(int * pixels) {
    free(pixels);
}