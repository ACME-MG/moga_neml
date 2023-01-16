"""
 Title:         The Trainer Factory
 Description:   For creating and returning trainer objects
 Author:        Janzen Choi

"""

# trainers
from modules.trainers.simple import Simple
from modules.trainers.strain import Strain

# Creates and return a trainer
def get_trainer(trainer_name, model):
    trainer_list = (
        Simple(model),
        Strain(model),
    )
    trainer_list = [trainer for trainer in trainer_list if trainer.get_name() == trainer_name]
    return trainer_list[0]