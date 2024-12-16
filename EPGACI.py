# Evolutionary Programming for Generating Accurately Censored Images


from ctypes import *
from PIL import Image
from time import sleep
import cv2
import numpy as np
import os
import random as rd

population_size = 20

lib = CDLL(os.path.realpath("EPGACI.so"))

c_int_p = POINTER(c_uint)
c_float_p = POINTER(c_float)

free_mem_func = c_int_p.in_dll(lib, "free_pixels")

lib.evaluate_fitness.restype = c_float
lib.mass_swap.restype = c_int_p
lib.smart_swap.restype = c_int_p

rng = np.random.default_rng()

class EPGACI:
    # stores each generation's best result
    stored_images = []
    # stores sorted pos
    sorted_pos = []
    # stores wins of individuals
    wins = []

    # constructor takes original image's file, the number of individuals to be generated, 
    # and the percentage of likeness desired
    def __init__(self, N, goal, generations, image):
        # original image's file
        self.orig_image_file = image
        # original image
        self.orig_image = Image.open(image).convert('RGB')
        # number of individuals in a population
        self.size = N
        # percentage of likeness desired
        self.goal = goal
        # number of generations of EPGACI
        self.generations = generations

    # show the original image
    def display_original(self):
        self.orig_image.show()

    # show best individual
    def display_best(self):
        Image.fromarray(self.best_ind).show()

    # show a generated individual from population as an images
    def display_individual(self, ind_pos):
        Image.fromarray(np.ctypeslib.as_array(self.population[ind_pos], shape=(self.height, self.width, 3)).astype(np.uint8)).show()
    
    # shows all generated individuals in population as images
    def display_population(self):
        for i in range(len(self.population)): self.display_individual(i)

    # prints individual using lib
    def print_individual(self, ind_pos):
        lib.print_individual(self.population[ind_pos].flatten().ctypes.data_as(c_int_p), self.num_pixels)
    
    # prints original using lib
    def print_original(self):
        lib.print_individual(self.orig_pixels_p, self.num_pixels)  
    
    # generates N number of individuals for initial population
    # uses mass_swap_mutate to randomly scramble the initial population
    def generate_population(self):
        # stores best individual
        self.best_ind = []
        # stores fitness of best individual
        self.best_fit = 100
        # population of images in the current generation
        self.population = []
        for i in range(self.size):
            self.population.append(self.orig_pixels_p)
            self.population[i] = self.mass_swap_mutate(i)

    # evaluates the fitness of an individual in the population using lib
    # fitness is how close the percentage of likeness an image (to the original)
    # is to the goal percentage of likeness
    def evaluate_fitness(self, ind_pos):
        fit = lib.evaluate_fitness(self.population[ind_pos], self.orig_pixels_p, c_double(self.goal), self.num_pixels)
        if fit < self.best_fit:
            self.best_ind = np.ctypeslib.as_array(self.population[ind_pos], shape=(self.height, self.width, 3)).astype(np.uint8)
            self.best_fit = fit
        self.fitness.append(fit)

    # evaluates the fitness of each individual in the population using lib
    def evaluate_population(self):
        # fitnesses of individuals in the current generation
        # goal is to be minimized
        self.fitness = []
        for i in range(self.size): self.evaluate_fitness(i)

    # mutation that swaps a random number of pixels (up to amount of pixels in image)
    def mass_swap_mutate(self, ind_pos):
        return lib.mass_swap(self.population[ind_pos], int(rd.random() * 1000), self.num_pixels)
    
    # swap mutation that swaps up to double the number of pixels needed to change (fitness)
    def smart_swap_mutate(self, ind_pos):
        if self.fitness[ind_pos] >= 1:
            max_pixels = self.num_pixels / self.fitness[ind_pos] * 2
        else:
            max_pixels = self.num_pixels * self.fitness[ind_pos] * 2
        return lib.smart_swap(self.population[ind_pos], int(rd.random() * 1000), int(max_pixels), self.num_pixels)

    # prints wins of each individual
    def print_wins(self):
        for i in range(len(self.fitness)): print(f"Individual {i+1} wins: {self.wins[i]}")
        print()
    
    # prints order of individuals based on wins
    def print_sorted(self):
        for i in range(len(self.fitness)):
            print(f"""Individual: {self.sorted_pos[i] + 1}
    fitness: {self.fitness[self.sorted_pos[i]]}  
    wins: {self.wins[self.sorted_pos[i]]}""")
        print()

    # generates children and adds them to the population
    # also performs repairs on children
    # takes number of iterations to decide which mutations to perform
    def generate_children(self, iters, total_iters):
        if iters < 3 * total_iters / 5:
            for i in range(self.size):
                self.population.append(self.mass_swap_mutate(i) if rd.randint(0,11) <= 8 else self.smart_swap_mutate(i))
                self.evaluate_fitness(self.size)
                self.size += 1
        else:
            for i in range(self.size):
                self.population.append(self.smart_swap_mutate(i) if rd.randint(0,11) <= 8 else self.mass_swap_mutate(i))
                self.evaluate_fitness(self.size)
                self.size += 1

    # round-robin tournament to assign wins to each individual
    # sets q: q = number of opponents to face
    # sets chance: chance of better individual winning (int 0-100)
    def round_robin(self, q, chance):
        self.q = q
        self.wins = []
        for i in range(self.size): 
            pos_used = []
            self.wins.append(0)
            for r in range(q):
                opp = i
                used = True
                while used:
                    opp = rd.randrange(self.size)
                    if opp is not i:
                        found = False
                        for u in range(r):
                            if pos_used[u] == opp: 
                                found = True
                                u = r
                        used = found
                if self.fitness[i] < self.fitness[opp]:
                    if rd.randrange(101) <= chance: self.wins[i] += 1
                elif self.fitness[i] == self.fitness[opp]:
                    if rd.randrange(2) == 0: self.wins[i] += 1
                else:
                    if rd.randrange(101) > chance: self.wins[i] += 1
                pos_used.append(opp)

    # sorts individuals by wins and stores sorted positions
    def sort_wins(self):
        self.sorted_pos = []
        for i in range(self.q, -1, -1):
            for k in range(self.size):
                if self.wins[k] == i: 
                    self.sorted_pos.append(k)

    # survivor selection: takes top N individuals to survive on
    def survivor_select(self):
        new_size = int (self.size / 2)
        for i in range(self.size-1, new_size-1, -1): lib.free_pixels(self.population[self.sorted_pos[i]])
        self.size = new_size
        self.population = [self.population[self.sorted_pos[i]] for i in range(self.size)]
        self.fitness = [self.fitness[self.sorted_pos[i]] for i in range(self.size)]

    # allows user to select portion of image to censor
    def select_portion(self):
        image = cv2.imread(self.orig_image_file)
        self.censor_coords = cv2.selectROI("Select Area to Censor\nPress Enter to Confirm", image, showCrosshair=False)
        self.censor_portion = self.orig_image.crop((int(self.censor_coords[0]), 
                                                    int(self.censor_coords[1]),
                                                    int(self.censor_coords[0]+self.censor_coords[2]),
                                                    int(self.censor_coords[1]+self.censor_coords[3])))
        cv2.destroyAllWindows()

    # initializes algorithm with the portion of image to censor
    def initialize(self):
        # width and height of all images
        self.width, self.height = self.censor_portion.size
        # number of pixels in all images
        self.num_pixels = self.width * self.height
        # original image's pixels stored as a 1D array (2D if considering each
        # pixel's individual values)
        self.orig_pixels = np.asarray(self.censor_portion).reshape((self.num_pixels, 3)).astype(c_uint)
        # original image's pixels converted to a flattened c_int_p
        self.orig_pixels_p = self.orig_pixels.flatten().ctypes.data_as(c_int_p)

    # attaches censored portion to original image
    def finish(self):
        self.orig_image.paste(Image.fromarray(self.best_ind), (int(self.censor_coords[0]), 
                                              int(self.censor_coords[1]),
                                              int(self.censor_coords[0]+self.censor_coords[2]),
                                              int(self.censor_coords[1]+self.censor_coords[3])))
        new_image = f"{self.goal} +- {self.best_fit}%.png"
        self.orig_image.save(new_image)

        path = os.path.realpath(new_image)
        os.startfile(path)
        sleep(3)
        os.remove(path)

    def run(self):
        self.select_portion()
        self.initialize()
        self.generate_population()
        self.evaluate_population()
        for i in range(self.generations):
            # mutation
            self.generate_children(i, self.generations)
            self.evaluate_population()
            # survivor selection
            self.round_robin(7, 100)
            self.sort_wins()
            self.survivor_select()
        self.finish()