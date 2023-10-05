"""
 Title:         The decreasing end constraint
 Description:   The constraint for ensuring that as a field increases,
                the end points of another field decreases 
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.constraints.__constraint__ import __Constraint__

# The decreasing end constraint class
class Constraint(__Constraint__):
    
    def initialise(self) -> None:
        """
        Runs at the start, once (optional placeholder)
        """
        self.x_label = self.get_x_label()
        self.y_label = self.get_y_label()
    
    def check(self, prd_data_list:list) -> bool:
        """
        Checks whether a constraint has been passed or not (must be overridden)
        
        Parameters:
        * `prd_data_list`: List of predicted data dictionaries
        
        Returns the results of the check
        """
        
        # Get map of stress to end point
        prd_dict = {}
        for prd_data in prd_data_list:
            prd_dict[self.x_label] = prd_data[self.y_label][-1]

        # Enforce that end points decrease as stress increases
        pass
        