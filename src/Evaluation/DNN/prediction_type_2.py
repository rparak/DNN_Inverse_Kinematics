# System (Default)
import sys
#   Add access if it is not in the system path.
if '../' + 'src' not in sys.path:
    sys.path.append('../..')
# Numpy (Array computing) [pip3 install numpy]
import numpy as np
# OS (Operating system interfaces)
import os
# SciencePlots (Matplotlib styles for scientific plotting) [pip3 install SciencePlots]
import scienceplots
# Matplotlib (Visualization) [pip3 install matplotlib]
import matplotlib.pyplot as plt
# Custom Script:
#   ../Lib/Parameters/Robot
import Lib.Parameters.Robot as Parameters
#   ../Lib/Kinematics/Core
import Lib.Kinematics.Core as Kinematics
#   ../Lib/Transformation/Utilities/Mathematics
import Lib.Transformation.Utilities.Mathematics as Mathematics
#   ../Lib/Trajectory/Utilities
import Lib.Trajectory.Utilities


"""
Description:
    Initialization of constants.
"""
# Set the structure of the main parameters of the robot.
CONST_ROBOT_TYPE = Parameters.EPSON_LS3_B401S_Str
# Save the data to a file.
CONST_SAVE_DATA = False
# Dataset configuration.
#   Number of data to be generated.
CONST_NUM_OF_DATA = 1000
#   Type of the dataset.
CONST_DATASET_TYPE = 1
#   The ID of the dataset in the selected type.
CONST_DATASET_ID = 0
# Initial and final time constraints.
CONST_T_0 = 0.0
CONST_T_1 = 1.0

# Absolute joint position start(id: 0) and stop(id: 1).
CONST_ABS_J_POS_0 = np.array([0.0, 0.0, 0.0, 0.0], dtype = np.float32)
CONST_ABS_J_POS_1 = np.array([Mathematics.Degree_To_Radian(90.0), Mathematics.Degree_To_Radian(0.0), 0.10, Mathematics.Degree_To_Radian(45.0)],
                              dtype = np.float32)

def main():
    """
    Description:
        ...
    """

    # Locate the path to the project folder.
    project_folder = os.getcwd().split('DNN_Inverse_Kinematics')[0] + 'DNN_Inverse_Kinematics'

    # Initialization of the structure of the main parameters of the robot.
    Robot_Str = CONST_ROBOT_TYPE

    # Initialization of the class to generate trajectory.
    Polynomial_Cls = Lib.Trajectory.Utilities.Polynomial_Profile_Cls(delta_time=0.01)
    
    # Set the parameters for the scientific style.
    plt.style.use(['science'])

    # Generation of multi-axis position trajectories from input parameters.
    theta_arr = []
    for i, (th_actual, th_desired) in enumerate(zip(CONST_ABS_J_POS_0, CONST_ABS_J_POS_1)):
        (theta_arr_i, _, _) = Polynomial_Cls.Generate(th_actual, th_desired, 0.0, 0.0, 0.0, 0.0,
                                                      CONST_T_0, CONST_T_1)
        theta_arr.append(theta_arr_i)

        # Create a figure.
        _, ax = plt.subplots()

        # Visualization of relevant structures.
        ax.plot(Polynomial_Cls.t, theta_arr[i], '.-', color='#d0d0d0', linewidth=1.0, markersize = 3.0, 
                markeredgewidth = 1.5, markerfacecolor = '#ffffff', label='...')

        # Parameters of the figure.
        #   Set the x ticks.
        ax.set_xticks(np.arange(np.min(Polynomial_Cls.t) - 0.1, np.max(Polynomial_Cls.t) + 0.1, 0.1))
        #   Set the y ticks.
        ax.set_yticks(np.arange(np.min(theta_arr[i]) - 0.1, np.max(theta_arr[i]) + 0.1, 0.1))
        #   Label.
        ax.set_xlabel(r't', fontsize=15, labelpad=10)
        ax.set_ylabel(r'$\theta_{%d}(t)$' % (i + 1), fontsize=15, labelpad=10) 
        #   Set parameters of the visualization.
        ax.grid(which='major', linewidth = 0.15, linestyle = '--')
        # Get handles and labels for the legend.
        handles, labels = plt.gca().get_legend_handles_labels()
        # Remove duplicate labels.
        legend = dict(zip(labels, handles))
        # Show the labels (legends) of the graph.
        ax.legend(legend.values(), legend.keys(), fontsize=10.0)

        if CONST_SAVE_DATA == True:
            # Set the full scree mode.
            plt.get_current_fig_manager().full_screen_toggle()

            # Save the results.
            plt.savefig(f'{project_folder}/src/Data/Prediction/{Robot_Str.Name}/Type_{CONST_DATASET_TYPE}/Config_N_{CONST_NUM_OF_DATA}_ID_{CONST_DATASET_ID}.png', format='png', dpi=300)
        else:
            # Show the result.
            plt.show()

if __name__ == "__main__":
    sys.exit(main())