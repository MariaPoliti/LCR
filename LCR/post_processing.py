import pandas as pd
import os
import time


def extract_output_signals(EIS_measurements):

    """
    Function to extract the primary and secondary outputs from the instrument.

    The actual output from the instrument is a list of values. For every
    measurement point collected,four outputs are provided. The first two are
    the actual measured values and the latter two refer to the status and the
    bin number. The latter two points are usually zero and will be removed
    in this funciton.


    Parameters
    ----------
    EIS_measurements: list
                      List outputted by the buffer memeory from the instrument

    Returns
    -------
    Z_magnitude: list
               List containing the values of the primary output from
               the instrument
               In this case it is the magnitude of the measured impedance
    Z_phase: list
              List containing the values of the secondary output from
              the instrument
              In this case it is the phase of the measured impedance


    Note: For each measurement, 4 entries are generated:

    Entry 1: Impedance Magnitude
    Entry 2: Phase Angle (rad)
    Entry 3&4: 0.0

    """
    # remove the empty entries [ 0.0 status and bin no. of every measurement.]
    EIS_measurements = [item for item in EIS_measurements if item != 0.0]

    # Extract the primary output
    Z_magnitude = [EIS_measurements[i] for i in range(len(EIS_measurements))
                   if i % 2 == 0]

    # Extract the secondary output
    Z_phase = [EIS_measurements[i] for i in range(len(EIS_measurements))
               if i % 2 != 0]

    return Z_magnitude, Z_phase


def gen_filename(sample, dist, temp):

    """
    Function to generate the string to use as the filename of the
    output file. The information contained in the filename are hardcoded
    to match our requirements, but can be easily changed.

    Parameters
    ----------
    sample: str
            String indicating the sample under investigation
    dist:  str
           String containing the distance between the two electrodes
    temp: str
          String representing the temperature the measurement was ran at

    Returns
    -------

    filename: str
              String to use as the filename of the current measurement

    """
    date = time.strftime('%y%m%d', time.localtime())
    filename = date + '_EIS_' + sample + '_' + dist + '_' + temp

    return filename


def write_file(freq, EIS_measurements, filename, save_location='./',
               comment=None):

    """
    Function that writes and saves a .csv file containing the results of the
    measurement. The units of the quantities being saved is indicated as
    metadata lines. Thes are hardcoed in this funciton.

    Parameters
    ----------
    freq: list
           List of frequencies to sweep over during the experiment.
    EIS_measurements: list
                      List outputted by the buffer memeory from the instrument.
    filename: str
              The name to use to save the .csv file with.
    save_location: str
                   Path to the folder the file will be save in. The default
                   value is the cwd.

    Rerurns
    -------
    If the all lines are correctly executed, the function will return
    a print statement.

    """
    if not os.path.exists(save_location):
        os.makedirs(save_location)

    magnitude, phase = extract_output_signals(EIS_measurements)
    to_file = {'frequency': freq, 'magnitude': magnitude, 'phase': phase}
    df_to_file = pd.DataFrame.from_dict(to_file)

    with open(save_location+filename + '.csv', mode='w',
              newline='') as f:
        f.write('frequency [Hz] \n')
        f.write('magnitude [ohm] \n')
        f.write('phase angle [rad] \n')
        if comment:
            comment = comment
        else:
            comment = 'None'
        f.write('Notes: ' + comment+'\n')
        df_to_file.to_csv(f)
        f.close()

    return print('The file was correctly saved')
