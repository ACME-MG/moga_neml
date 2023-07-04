"""
 Title:         Multi-Objective Genetic Algorithm
 Description:   For parameter optimisation
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import warnings
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.optimize import minimize
from moga_neml._optimise.problem import Problem

# The Multi-Objective Genetic Algorithm (MOGA) class
class MOGA:
    
    # Constructor
    def __init__(self, problem:Problem, num_gens:int, init_pop:int, offspring:int, crossover:float, mutation:float):
        
        # Initialise
        self.problem    = problem
        self.controller = problem.get_controller()
        self.param_dict = self.controller.get_model().get_param_dict()
        self.num_gens   = num_gens
        self.init_pop   = init_pop
        self.offspring  = offspring
        self.crossover  = crossover
        self.mutation   = mutation

        # Gets initialised parameters
        init_param_dict = self.controller.get_set_param_dict()
        population = self.get_population(init_param_dict)

        # Define algorithm
        self.algo = NSGA2(
            pop_size     = init_pop,
            n_offsprings = offspring,
            sampling     = population,
            crossover    = SBX(prob=crossover, prob_var=1.0), # simulated binary crossover 
            mutation     = PolynomialMutation(prob=mutation), # polynomial mutation
            eliminate_duplicates = True
        )

    # Given a set of parameters, returns a population with some deviation
    def get_population(self, init_param_dict:dict) -> tuple:
        
        # Initialise
        mean_list  = []
        stdev_list = []
        
        # Determine mean and std values
        for param_name in self.param_dict.keys():
            
            # If the user defined a starting value
            if param_name in init_param_dict.keys():
                mean_list.append(init_param_dict[param_name]["value"])
                stdev_list.append(init_param_dict[param_name]["std"])
            
            # Otherwise, define normal sampling
            else:
                mid_point = (self.param_dict[param_name]["u_bound"] + self.param_dict[param_name]["l_bound"]) / 2
                bound_range = self.param_dict[param_name]["u_bound"] - self.param_dict[param_name]["l_bound"]
                mean_list.append(mid_point)
                stdev_list.append(bound_range/4) # std ~= range / 4

        # Create the population
        param_population = np.random.normal(
            loc   = np.array(mean_list),
            scale = np.array(stdev_list),
            size  = (self.init_pop, len(self.param_dict.keys())),
        )
        
        # Clamp the population by the bounds
        for i in range(len(param_population)):
            for j in range(len(self.param_dict.keys())):
                param_name = list(self.param_dict.keys())[j]
                l_bound = self.param_dict[param_name]["l_bound"]
                u_bound = self.param_dict[param_name]["u_bound"]
                param_population[i][j] = max(min(param_population[i][j], u_bound), l_bound)
                
        # Return the population
        return param_population

    # Runs the genetic optimisation
    def optimise(self) -> None:
        warnings.filterwarnings("ignore")
        minimize(self.problem, self.algo, ("n_gen", self.num_gens), verbose=False, seed=None)