import time


def cable_length(my_instrument, length=1):
    """
    Function to activate the cable length correction.
    The correction will then be active on the intrument.
    Unless tuned off, the correction will be applied to all the measurements
    collected after.

    Parameters
    ----------
    my_instrument: pyvisa.resources.usb.USBInstrument
                   Instrument instance obtained throught the Pyvisa package
    mode: str
          Options are ON or OFF.
    length: int
            Set the length of the cable to correct for. Options are 0 to 4 m

    Returns
    -------
    The function will return a print statement confirming the
    task was completed.
    """
    # Clear previous states and resets the instrument settings
    my_instrument.write('*RST; *CLS')

    # Enable the display to update itself when a change is made
    my_instrument.write(':DISP:ENAB')
    time.sleep(3)

    # Configure the instrument to automatically perform continuous
    # measurements
    my_instrument.write(':INIT:CONT')

    # * Switch the instrument triggering function to 'EXT'
    # in order to control the measurements remotely
    my_instrument.write(':TRIG:SOUR EXT')
    time.sleep(5)
    my_instrument.write(':CORR:LENG ', length)

    return print('the correction for the cable length was set to {}'
                 .format(length))


def open(my_instrument, mode='ON', collect=False):
    """
    Function to activate and measure the open circuit potential
    (OCP) of the system. The correction will then be active
    on the intrument. Once this funciton is ran, the new OCP
    will be stored in the instrument and unless tuned off,
    the correction will be applied to all the measurements collected after.

    Parameters
    ----------

    my_instrument: pyvisa.resources.usb.USBInstrument
                   Instrument instance obtained throught the Pyvisa package
    mode: str
          Options are ON or OFF.
    collect: bool
             Option to collect  a new measurement for the open correction.
             If collect is set to false, the last measured open correction will
             be used.

    Returns
    -------
    The function will return a print statement confirming the
    task was completed.
    """

    # Clear previous states and resets the instrument settings
    my_instrument.write('*RST; *CLS')

    # Enable the display to update itself when a change is made
    my_instrument.write(':DISP:ENAB')
    time.sleep(3)

    # Configure the instrument to automatically perform continuous
    # measurements
    my_instrument.write(':INIT:CONT')

    # * Switch the instrument triggering function to 'EXT'
    # in order to control the measurements remotely
    my_instrument.write(':TRIG:SOUR EXT')
    time.sleep(5)
    if mode == 'ON':
        my_instrument.write(':CORR:OPEN:STAT ON')
        if collect:
            my_instrument.write(':CORR:OPEN:EXEC')
        else:
            pass

        return print('the correction for the Open Circuit Potential' +
                     ' was successfully collected')
    else:
        my_instrument.write(':CORR:OPEN:STAT OFF')

        return print('the correction for the Open Circuit Potential' +
                     ' was disactivated')


def short(my_instrument, mode='ON', collect=False):

    """
    Function to activate and measure a short circuit correction for
    the system. The correction will then be active
    on the intrument. Once this funciton is ran, the short correction
    will be stored in the instrument and unless tuned off,
    the correction will be applied to all the measurements collected after.

    Parameters
    ----------

    my_instrument: pyvisa.resources.usb.USBInstrument
                   Instrument instance obtained throught the Pyvisa package
    mode: str
          Options are ON or OFF.
    collect: bool
             Option to collect a new measurement for the open correction.
             If collect is set to false, the last measured open correction will
             be used.

    Returns
    -------
    The function will return a print statement confirming the
    task was completed.
    """

    # Clear previous states and resets the instrument settings
    my_instrument.write('*RST; *CLS')

    # Enable the display to update itself when a change is made
    my_instrument.write(':DISP:ENAB')
    time.sleep(3)

    # Configure the instrument to automatically perform continuous
    # measurements
    my_instrument.write(':INIT:CONT')

    # * Switch the instrument triggering function to 'EXT'
    # in order to control the measurements remotely
    my_instrument.write(':TRIG:SOUR EXT')
    time.sleep(5)
    if mode == 'ON':
        my_instrument.write(':CORR:SHOR:STAT ON')
        if collect:
            my_instrument.write(':CORR:SHOR:EXEC')
        else:
            pass

        return print('the correction for the short correction' +
                     'was successfully collected')
    else:
        my_instrument.write(':CORR:SHOR:STAT OFF')

        return print('the correction for the short correction' +
                     'was disactivated')
