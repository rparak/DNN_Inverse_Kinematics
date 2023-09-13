# OS (Operating system interfaces)
import os
# Typing (Support for type hints)
import typing as tp
# Tensorflow (Machine learning) [pip3 install tensorflow]
import tensorflow as tf
# Scikit-Optimize, or skopt (Sequential model-based optimization) [pip3 install scikit-optimize]
import skopt
# Joblib (Lightweight pipelining) [pip3 install joblib]
import joblib
# Sklearn (Simple and efficient tools for predictive data analysis) [pip3 install scikit-learn]
import sklearn.model_selection
# Custom Script:
#   ../Lib/DNN_IK/Utilities
import Lib.DNN_IK.Utilities as Utilities

"""
Description:
    Initialization of constants.
"""
# Locate the path to the project folder.
CONST_PROJECT_FOLDER = os.getcwd().split('DNN_Inverse_Kinematics')[0] + 'DNN_Inverse_Kinematics'

class DCNN_Trainer_Cls(object):
    """
    Description:
        densely-connected neural network (DCNN)

    Initialization of the Class:
        Args:
            (1) ... [...]: ...
            (..) file_path [string]: The specified path of the file without extension (format).

        Example:
            Initialization:
                # Assignment of the variables.
                ...

                # Initialization of the class.
                Cls = DCNN_Train_Cls()

            Features:
                # Properties of the class.
                ...

                # Functions of the class.
                ...
    """
        
    def __init__(self, x: tp.List[float], y: tp.List[float], train_size: float, test_size: float,
                 file_path: str) -> None:
        
        # A variable that indicates that validation data will also be used for training.
        self.__use_validation = False if test_size == 0.0 else True

        # Split the data from the dataset (x, y) into random train and validation subsets.
        if self.__use_validation == True:
            self.__x_train, self.__x_validation, self.__y_train, self.__y_validation = sklearn.model_selection.train_test_split(x, y, train_size=train_size, test_size=test_size, 
                                                                                                                                random_state=0)
            
        else:
            self.__x_train = x; self.__y_train = y

        # Find the scale parameter from the dataset and transform the data using this parameter.
        self.__scaler_x, self.__x_train_scaled = Utilities.Scale_Data([-1.0, 1.0], self.__x_train)
        self.__scaler_y, self.__y_train_scaled = Utilities.Scale_Data([-1.0, 1.0], self.__y_train)
        
        # The file path to save the data.
        self.__file_path = file_path

        # Set whether memory growth should be enabled.
        gpu_arr = tf.config.experimental.list_physical_devices('GPU')
        if gpu_arr:
            for _, gpu_i in enumerate(gpu_arr):
                tf.config.experimental.set_memory_growth(gpu_i, True)
        else:
            print('[INFO] No GPU device was found.')

        # Initialization of a sequential neural network model.
        self.__model = tf.keras.models.Sequential()

        if self.__use_validation == True:
            # Transform of data using an the scale parameter.
            self.__x_validation_scaled = Utilities.Transform_Data_With_Scaler(self.__scaler_x, self.__x_validation)
            self.__y_validation_scaled = Utilities.Transform_Data_With_Scaler(self.__scaler_y, self.__y_validation)

            # A callback to save the model with a specific frequency.
            self.__callback = tf.keras.callbacks.ModelCheckpoint(filepath=f'{self.__file_path}_use_val_{self.__use_validation}.h5', monitor='val_loss', save_best_only=True, 
                                                                 verbose=1)
        else:
            self.__callback = tf.keras.callbacks.ModelCheckpoint(filepath=f'{self.__file_path}_use_val_{self.__use_validation}.h5', monitor='loss', save_best_only=True, 
                                                                 verbose=1)   
        
    def Save(self):

        # Save the scaler parameter for input/output data.
        joblib.dump(self.__scaler_x, f'{self.__file_path}_use_val_{self.__use_validation}_Scaler_x.pkl')
        joblib.dump(self.__scaler_y, f'{self.__file_path}_use_val_{self.__use_validation}_Scaler_y.pkl')

        # Save a model (image) of the neural network architecture.
        tf.keras.utils.plot_model(self.__model, to_file=f'{self.__file_path}_use_val_{self.__use_validation}_Architecture.png', show_shapes=True, show_layer_names=True)

    def __Release(self) -> None:
        """
        Description:
            Function to release GPU resources when the training process is already complete.
        """

        tf.keras.backend.clear_session()

    def Build(self, Hyperparameters: tp.Dict) -> None:
        """
        Description:
            ...
        """
                
        pass

    def Train(self, epochs: int, batch_size: int) -> None:
        """
        Description:
            ...
        """
                
        if self.__use_validation == True:
            self.__model.fit(self.__x_train_scaled, self.__y_train_scaled, epochs=epochs, batch_size=batch_size, verbose=1, 
                             validation_data=(self.__x_validation_scaled, self.__y_validation_scaled), callbacks = [self.__callback])
        else:
            self.__model.fit(self.__x_train_scaled, self.__y_train_scaled, epochs=epochs, batch_size=batch_size, verbose=1,
                             callbacks = [self.__callback])

        # Release GPU resources when the training process is already complete.
        self.__Release()

class DCNN_Predictor_Cls(object):
    """
    Description:
        ...

    Initialization of the Class:
        Args:
            (1) ... [...]: ...

        Example:
            Initialization:
                # Assignment of the variables.
                ...

                # Initialization of the class.
                Cls = DNN_Cls()

            Features:
                # Properties of the class.
                ...

                # Functions of the class.
                ...
    """
        
    def __init__(self) -> None:
        pass  

class DCNN_Tuner_Cls(object):
    """
    Description:
        ...

    Initialization of the Class:
        Args:
            (1) ... [...]: ...

        Example:
            Initialization:
                # Assignment of the variables.
                ...

                # Initialization of the class.
                Cls = DNN_Cls()

            Features:
                # Properties of the class.
                ...

                # Functions of the class.
                ...
    """
        
    def __init__(self) -> None:
        pass