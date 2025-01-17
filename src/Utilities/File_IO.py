# Numpy (Array computing) [pip3 install numpy]
import numpy as np
# Typing (Support for type hints)
import typing as tp
# Pickle (Python object serialization)
import pickle as pkl

def Load(file_path: str, format: str, separator: str) -> tp.List[tp.Union[float, bool]]:
    """
    Description:
        A simple function to read data from the file.

        Note:
            Deserialization of the data into a binary / text file.

    Args:
        (1) file_path [string]: The specified path of the file without extension (format).
        (2) format [string]: The format of the loaded file.
                             Note:
                                'pkl' : Pickle file; 'txt' : Text file
        (3) separator [string]: Separator between data.

    Returns:
        (1) parameter [Dictionary of different types of data <float, bool, etc.>]: Loaded data from a binary file.
    """

    if format == 'pkl':
        # Open the file in 'rb' mode (read binary). 
        with open(file_path + f'.{format}', 'rb') as f:
            # Load the data from the file using the file object (f).
            data_tmp = pkl.load(f)

    elif format == 'txt':
        data_tmp = []
        with open(file_path + f'.{format}', 'r') as f:
            # Read the line of the file in the current step.
            for line in f:
                # Splits a string into a list with the specified delimiter (,) 
                # and converts to a float.
                data_tmp.append(np.float64(line.split(separator)))

    # Convert a list to an array.
    data = np.array(data_tmp, dtype=np.float64)
    
    # Close the file after loading the data.
    f.close()

    return data

def Save(file_path: str, data: tp.List[tp.Union[float, bool]], format: str, separator: str) -> None:
    """
    Description:
        A simple function to write data to the file.

        Note:
            Serialization of the data into a binary / text file.

    Args:
        (1) file_path [string]: The specified path of the file without extension (format).
        (2) data [Dictionary of different types of data <float, bool, etc.>]: Individual data.
        (3) format [string]: The format of the saved file.
                             Note:
                                'pkl' : Pickle file; 'txt' : Text file, 'urdf' : Unified Robotics Description Format.
        (3) separator [string]: Separator between data.
    """
    
    if format == 'pkl':
        # Open the file in 'wb' mode (write binary). 
        with open(file_path + f'.{format}', 'wb') as f:
            # Write the input data to a file using the file object (f).
            pkl.dump(data, f)
    elif format in ['txt', 'urdf']:
        with open(file_path + f'.{format}', 'a+') as f:
            # Write the data to the file.
            for data_i in data[:-1]:
                f.writelines([str(data_i), separator])
            f.writelines([str(data[-1]), '\n'])

    # Close the file after writing the data.
    f.close()