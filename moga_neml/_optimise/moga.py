"""
 Title:         Multi-Objective Genetic Algorithm
 Description:   For parameter optimisation
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.lhs import LHS
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
        self.objective  = problem.get_objective()
        self.num_gens   = num_gens
        self.init_pop   = init_pop
        self.offspring  = offspring
        self.crossover  = crossover
        self.mutation   = mutation

        # Gets initialised parameters
        init_param_dict = self.objective.get_init_param_dict()
        print(self.get_custom_population(init_param_dict))

        # Define algorithm
        self.algo = NSGA2(
            pop_size     = init_pop,
            n_offsprings = offspring,
            sampling     = LHS(),                               # latin hypercube sampling
            crossover    = SBX(prob=crossover, prob_var=1.0),   # simulated binary crossover 
            mutation     = PolynomialMutation(prob=mutation),   # polynomial mutation
            eliminate_duplicates = True
        )

    # Given a set of parameters, returns a population with some deviation
    #   TODO ACCOUNT FOR WHEN SOME PARAMETERS ARE NOT INITIALISED
    def get_custom_population(self, initial_param_dict:dict) -> tuple:
        
        # Initialise
        param_dict = self.objective.get_param_dict()
        mean_list  = []
        stdev_list = []
        
        # Determine mean and std values
        for param_name in param_dict.keys():
            
            # If the user defined a starting value
            if param_name in initial_param_dict.keys():
                mean_list.append(initial_param_dict[param_name])
                stdev_list.append(0)
            
            # Otherwise, define normal sampling
            else:
                mid_point = (param_dict[param_name]["u_bound"] + param_dict[param_name]["l_bound"]) / 2
                range = param_dict[param_name]["u_bound"] - param_dict[param_name]["l_bound"]
                mean_list.append(mid_point)
                stdev_list.append(range/2)

        # Create the population and return it
        param_population = np.random.normal(
            loc   = np.array(mean_list),
            scale = np.array(stdev_list),
            size  = (self.init_pop, len(param_dict.keys())),
        )
        return param_population

    # Runs the genetic optimisation
    def optimise(self) -> None:
        minimize(self.problem, self.algo, ("n_gen", self.num_gens), verbose=False, seed=None)