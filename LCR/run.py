import pyvisa
import time

from LCR import frequency


def instrument_conection():
    """
    Function to make connection wiht the instrument and ensure that commands
    can be correctly delivered to it.

    Parameters
    ----------
    None. Just ensure that the instrument is conencted through the device USB
    port.

    Returns
    -------
    my_instrument: pyvisa.resources.usb.USBInstrument
                   Instrument instance obtained throught the Pyvisa package

    """
    # Connect the instrument and ensure you can comunicate wiht it
    rm = pyvisa.ResourceManager
    inst = rm.list_resources()
    if len(inst) != 0:
        print('The is/are \033[1m{}\033[0m insturment(s)' +
              ' conencted to this device.'.format(len(inst)))

        # If only one instrument is connected to the computer,
        # the argument can be replaced
        my_instrument = rm.open_resource(rm.list_resources()[0])

        # The next line is only to confirm that the correct instrument
        # is connected to the computer
        print('\nThe selected instrument is: \033[1m {}'.format(
            my_instrument.query('*IDN?')))

        # Define the termination format - new line
        my_instrument.read_termination = '\n'
        my_instrument.write_termination = '\n'
        my_instrument.query('*IDN?')
        # Setting the instrument timeout to 100000. This way the conenction
        # to the instrument won't be interrupted while the data is collected
        my_instrument.timeout = 100000

        return my_instrument
    else:
        return print('No instrument was found.\nEnsure the instrument is' +
                     'correctly connected to your device and try again')


def measurement(my_instrument, function, frequencies, input_signal='voltage',
                amplitude=0.01):

    """
    Function to set up and collect a measurement using the isntrument connected
    to your device.

    Parameters
    ----------
    my_instrument: pyvisa.resources.usb.USBInstrument
                   Instrument instance obtained throught the Pyvisa package
    function: str
              String indicating to the instrument which measurement to collect
    frequencies: list
               variable containing the list of frequency to use in the
               measurement. The list will be
               converted into one within this function
    input_signal: str
                  Option of voltage or current
    aplitude: int or float
              Amplitude of the input signal. Either current or voltage

    Returns
    -------
    output_signals: list
                    list containing the output measurements from the instrument
    """

    # Clear previous states and resets the instrument settings
    my_instrument.write('*RST; *CLS')

    # Enable the display to update itself when a change is made
    my_instrument.write(':DISP:ENAB')
    time.sleep(2)

    # Configure the instrument to automatically perform continuous
    # measurements
    my_instrument.write(':INIT:CONT')

    # * Switch the instrument triggering function to 'EXT'
    # in order to control the measurements remotely
    my_instrument.write(':TRIG:SOUR EXT')
    time.sleep(2)

    # Choose the function we want to use for the experimental run.
    # In this case we are going to be runnin an Electrochemical
    # Impedance Spectrum by measuring the magnitude and the phase angle
    # - in radians
    my_instrument.write(':FUNC:IMP:TYPE ', function)

    # Set the input voltage amplitude by runnning the following cell.
    if input_signal == 'votlage' or 'Voltage' or 'V':
        my_instrument.write(':VOLT:LEVEL ', str(amplitude))
        time.sleep(2)
    else:
        my_instrument.write(':CURR:LEVEL ', str(amplitude))
        time.sleep(2)

    # Set the measurement time to medium
    my_instrument.write(':APER MED')

    # Set the impedance range to automatic
    my_instrument.write(':FUNC:IMP:RANGE:AUTO ON')
    time.sleep(2)

    # Displays the list page. Once you set the list of
    # freqeuncies you want to scan over, the list page should be
    # automatically updated
    my_instrument.write(':DISP:PAGE LIST')
    my_instrument.write(':FORM:DATA ASC')
    my_instrument.write(':LIST:MODE SEQ')
    time.sleep(2)

    # Set the frequency you want to run the impedance measurement at
    # if isinstance(type(frequencies), str):
    #     my_instrument.write('LIST:FREQ ', frequencies)
    # else:
    frequencies = frequency.freq_str(frequencies)
    my_instrument.write('LIST:FREQ ', frequencies)

    time.sleep(2)

    # Set the source of the memory to external.
    my_instrument.write(':MMEM EXT')

    # We are gonna use the memory buffer as I am going to independently
    # save the data into a single file instead of having the instrument
    # do that for me. Giving dimensions to the buffer memory ensures
    # that only the data collected is going to be save.
    my_instrument.write(':MEM:DIM DBUF, ', str(len(frequencies)))

    # Initialize the memory log for the given frequency list indicated above
    my_instrument.write(':MEM:FILL DBUF')
    time.sleep(2)

    # Triggers the instrument to run the measurement
    my_instrument.write(':TRIG:IMM')
    time.sleep(2)

    # Save the data we just collected into a variable
    output_signals = my_instrument.query_ascii_values(':MEM:READ? DBUF')
    time.sleep(5)

    # * Let's clean the memory buffer and return to the display page
    my_instrument.write(':MEM:CLE DBUF')
    my_instrument.write(':DISP:PAGE MEAS')

    return output_signals


def cancel_measurement(my_instrument):
    """
    Funciton to cancel any mesurementbeing taken by the isntrument.

    Parameters
    ----------
    my_instrument: pyvisa.resources.usb.USBInstrument
                   Instrument instance obtained throught the Pyvisa package

    Returns
    -------
    A print statement to confirm that the command was correctly sent to the
    instrument
    """
    my_instrument.write(':ABOR')

    return print('Measurement cancelled')
