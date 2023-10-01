# System (Default)
import sys
#   Add access if it is not in the system path.
if '..' + 'src' not in sys.path:
    sys.path.append('..')
# OS (Operating system interfaces)
import os
# Custom Script:
#   ../Lib/Parameters/Robot
import Lib.Parameters.Robot
#   ../Lib/Utilities/File_IO
import Lib.Utilities.File_IO as File_IO
#   ../Lib/FCNN_IK/Model
import Lib.FCNN_IK.Model
#   ../Hyperparameters/EPSON_LS3_B401S
import Hyperparameters.EPSON_LS3_B401S

"""
Description:
    Initialization of constants.
"""
# Set the structure of the main parameters of the robot.
CONST_ROBOT_TYPE = Lib.Parameters.Robot.EPSON_LS3_B401S_Str
# Dataset configuration.
#   Number of data to be generated.
CONST_NUM_OF_DATA = 1000
#   Method to be used for training.
#       Method 0: No test (validation) partition.
#       Method 1: With test (validation) partition.
CONST_DATASET_METHOD = 0

def main():
    """
    Description:
        A program for training an Inverse Kinematics (IK) task using a Fully-Connected Neural Network (FCNN).
    """

    # Locate the path to the project folder.
    project_folder = os.getcwd().split('FCNN_Inverse_Kinematics')[0] + 'FCNN_Inverse_Kinematics'

    # Initialization of the structure of the main parameters of the robot.
    Robot_Str = CONST_ROBOT_TYPE

    # Create a file path to read/write the data.
    file_path_r = f'{project_folder}/src/Data/Dataset/{Robot_Str.Name}/Config_N_{CONST_NUM_OF_DATA}'
    file_path_w = f'{project_folder}/src/Data/Model/{Robot_Str.Name}/Config_N_{CONST_NUM_OF_DATA}'

    # Read the data from a file.
    data = File_IO.Load(file_path_r, 'pkl', ',')

    # Assign data to variables.
    #   Input of the NN:  x -> Position(x, y, z); Orientation(quaternion)
    #   Output of the NN: y -> theta(0 .. n)
    x = data[:, 0:7].astype('float32'); y = data[:, -Robot_Str.Theta.Zero.size:].astype('float32')

    # Train the Fully-Connected Neural Network (FCNN) model.
    #   1-2\ Initialization and Compilation.
    if CONST_DATASET_METHOD == 0:
        FCNN_IK_Trainer_Cls = Lib.FCNN_IK.Model.FCNN_Trainer_Cls(x=x, y=y, train_size=1.0, test_size=0.0, 
                                                                 file_path=file_path_w)
        FCNN_IK_Trainer_Cls.Compile(Hyperparameters.EPSON_LS3_B401S.FCNN_HPS_METHOD_0)
    elif CONST_DATASET_METHOD == 1:
        FCNN_IK_Trainer_Cls = Lib.FCNN_IK.Model.FCNN_Trainer_Cls(x=x, y=y, train_size=0.8, test_size=0.2, 
                                                                 file_path=file_path_w)
        FCNN_IK_Trainer_Cls.Compile(Hyperparameters.EPSON_LS3_B401S.FCNN_HPS_METHOD_1)
    #   3\ Train.
    FCNN_IK_Trainer_Cls.Train(epochs=10000, batch_size=64)
    #   4\ Save.
    FCNN_IK_Trainer_Cls.Save()

if __name__ == "__main__":
    sys.exit(main())
