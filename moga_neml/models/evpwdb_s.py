"""
 Title:         The Elastic Viscoplastic Work Damage Model with bilinear function for work damage
 Description:   Incorporates elasto-viscoplasticity and work damage
 Author:        Janzen Choi

"""

# Libraries
import numpy as np, math
from moga_neml.io.plotter import Plotter
from moga_neml.models.__model__ import __Model__
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow, damage, interpolate

# Constants
CIRCLE_INTERVAL = 20

# The Elastic Visco Plastic Work Damage Class
class Model(__Model__):

    def initialise(self):
        """
        Runs at the start, once
        """

        # Elastic parameters
        self.add_param("evp_s0",  0.0e0, 1.0e2) # 3 (</ 1e2)
        self.add_param("evp_R",   0.0e0, 1.0e3) # 4
        self.add_param("evp_d",   0.0e0, 1.0e2) # 2
        self.add_param("evp_n",   1.0e0, 1.0e2) # 2
        self.add_param("evp_eta", 0.0e0, 1.0e4) # 5
        
        # Critical work parameters
        self.add_param("c_0", 0e0, 1.0e3)
        self.add_param("c_1", 0e0, 1.0e3)
        self.add_param("t_0", 0e0, 1.0e3)
        self.add_param("t_1", 0e0, 1.0e3)

        # Exponent parameters
        self.add_param("n_0", 0.0e0, 1.0e2)
        self.add_param("n_1", 0.0e0, 1.0e2)

    def calibrate_model(self, evp_s0:float, evp_R:float, evp_d:float, evp_n:float, evp_eta:float,
                        c_0:float, c_1:float, t_0:float, t_1:float, n_0:float, n_1:float):
        """
        Gets the predicted curves

        Parameters:
        * `evp_s0`:  Initial yield stress
        * `evp_R`:   Isotropic hardening stress
        * `evp_d`:   Isotropic hardening rate
        * `evp_n`:   Rate sensitivity
        * `evp_eta`: Viscoplastic fluidity
        * `c_0`:     Gradient for left side of bilinear function
        * `c_1`:     Vertical intercept for left side of bilinear function
        * `t_0`:     Gradient for right side of bilinear function
        * `t_1`:     Vertical intercept for right side of bilinear function
        * `n_0`:     The gradient of the n curve
        * `n_1`:     The intercept of the n curve

        Returns the calibrated model
        """

        # If tensile shelf is not higher than creep shelf, then bad parameters
        if t_0 < c_0 or t_1 < c_1:
            return
        
        # Define EVP model
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs",
                                                               self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        
        # Gets the interpolators
        wr_list = get_wr_list(c_0, c_1, t_0, t_1)
        wc_list = [get_wc(wr, c_0, c_1, t_0, t_1) for wr in wr_list]
        n_list  = [get_n(wr, n_0, n_1) for wr in wr_list]
        wr_list = [math.pow(10, wr) for wr in wr_list]
        wd_wc   = interpolate.PiecewiseSemiLogXLinearInterpolate(wr_list, wc_list)
        wd_n    = interpolate.PiecewiseSemiLogXLinearInterpolate(wr_list, n_list)
        
        # Define work damage model and return
        wd_model = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=False, eps=1e-40, work_scale=1e5)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model

    def record_results(self, output_path:str, evp_s0:float, evp_R:float, evp_d:float, evp_n:float, evp_eta:float,
                        c_0:float, c_1:float, t_0:float, t_1:float, n_0:float, n_1:float) -> None:
        """
        Records the interpolators

        Parameters:
        * `output_path`: The path to the output directory
        * `evp_s0`:  Initial yield stress
        * `evp_R`:   Isotropic hardening stress
        * `evp_d`:   Isotropic hardening rate
        * `evp_n`:   Rate sensitivity
        * `evp_eta`: Viscoplastic fluidity
        * `c_0`:     Gradient for left side of bilinear function
        * `c_1`:     Vertical intercept for left side of bilinear function
        * `t_0`:     Gradient for right side of bilinear function
        * `t_1`:     Vertical intercept for right side of bilinear function
        * `n_0`:     The gradient of the n curve
        * `n_1`:     The intercept of the n curve

        Returns the calibrated model
        """

        # Gets the interpolators
        wr_list = get_wr_list(c_0, c_1, t_0, t_1)
        wc_list = [get_wc(wr, c_0, c_1, t_0, t_1) for wr in wr_list]
        n_list  = [get_n(wr, n_0, n_1) for wr in wr_list]
        wr_list = [math.pow(10, wr) for wr in wr_list]

        # Plot wr-wc
        wc_plotter = Plotter(f"{output_path}/critical_work.png", "Work Rate", "Critical Work")
        wc_plotter.prep_plot()
        wc_plotter.scat_plot({"Work Rate": wr_list, "Critical Work": wc_list})
        wc_plotter.set_log_scale(x_log=True)
        wc_plotter.save_plot()
        wc_plotter.clear()

        # Plot wr-wc
        wc_plotter = Plotter(f"{output_path}/damage_exponent.png", "Work Rate", "Damage Exponent")
        wc_plotter.prep_plot()
        wc_plotter.scat_plot({"Work Rate": wr_list, "Damage Exponent": n_list})
        wc_plotter.set_log_scale(x_log=True)
        wc_plotter.save_plot()
        wc_plotter.clear()

def get_bounds(c_0:float, c_1:float, t_0:float, t_1:float) -> tuple:
    """
    Gets the interpolation bilinear points
    
    Parameters:
    * `c_0`: Gradient for left side of bilinear function
    * `c_1`: Vertical intercept for left side of bilinear function
    * `t_0`: Gradient for right side of bilinear function
    * `t_1`: Vertical intercept for right side of bilinear function
    
    Returns the intervals of the interpolation
    """
    wr_0 = -c_1/c_0
    wr_1 = (t_1-c_1) / (c_0-t_0)
    wr_2 = 5
    return wr_0, wr_1, wr_2

def get_wc(wr:float, c_0:float, c_1:float, t_0:float, t_1:float) -> float:
    """
    Gets the critical work
    
    Parameters:
    * `wr`:  The work rate value
    * `c_0`: Gradient for left side of bilinear function
    * `c_1`: Vertical intercept for left side of bilinear function
    * `t_0`: Gradient for right side of bilinear function
    * `t_1`: Vertical intercept for right side of bilinear function
    
    Returns the critical work
    """
    wr_0, wr_1, wr_2 = get_bounds(c_0, c_1, t_0, t_1)
    if wr <= wr_0 + 1:
        return c_0 * math.exp(wr - wr_0 - 1)
    elif wr_0 + 1 < wr and wr <= wr_1:
        return c_0*wr + c_1
    elif wr_1 and wr <= wr_2:
        return t_0*wr + t_1
    else:
        return 0

def get_wr_list(c_0:float, c_1:float, t_0:float, t_1:float) -> list:
    """
    Gets the work rate values
    
    Parameters:
    * `c_0`: Gradient for left side of bilinear function
    * `c_1`: Vertical intercept for left side of bilinear function
    * `t_0`: Gradient for right side of bilinear function
    * `t_1`: Vertical intercept for right side of bilinear function
    
    Returns the work rate values
    """
    wr_0, wr_1, wr_2 = get_bounds(c_0, c_1, t_0, t_1)
    interval_size = 32
    wr_list = list(np.linspace(wr_0-5, wr_0+1, interval_size)) +\
              list(np.linspace(wr_0+1, wr_1, interval_size)) +\
              list(np.linspace(wr_1, wr_2, interval_size))
    return wr_list

def get_n(wr:float, n_0:float, n_1:float) -> float:
    """
    Gets the exponent value
    
    Parameters:
    * `wr`:  The work rate value
    * `n_0`: The gradient of the n curve
    * `n_1`: The intercept of the n curve
    
    Returns the exponent
    """
    return n_0*wr + n_1
