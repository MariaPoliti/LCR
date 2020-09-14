import numpy as np


def freq_list(high_freq, low_freq, pts_per_decade=10):
    '''
    Function that generates the frequency range used to investigate the
    impedance response of an electrical circuit Frequency Generator with
    log-spaced frequencies

    Parameters
    ----------
    high_freq: single value (int or float)
               Initial frequency value (high frequency domain) [Hz]
    high_freq: single value (int or float)
               Final frequency value (low frequency domain) [Hz]
    pts_per_decade: integer
                    Number of frequency decades to be used as range.
                    Default value is set to be 10

    Returns
    ----------
    freq_list: list
               List of frequency [Hz] linearly spaced on a base-ten
               logarithm scale

    '''
    # determine the number of decades based on the two frequency extremes
    # provided as input to the function
    f_decades = int(np.log10(int(high_freq)) - np.log10(low_freq))
    # Generate the array of frequencies linearly spaced on a log10 scale
    f_range = np.logspace(np.log10(int(high_freq)), np.log10(low_freq),
                          np.around(pts_per_decade*f_decades), endpoint=True)
    # Convert the array into a list of frequencies and reduced the number of
    # digits displayed for each entry
    freq_list = [np.round(item, 6) for item in f_range]

    return freq_list


def freq_str(freq_list):

    """
    Function that transforms the array of frequency values into a string
    of comma separated entries.

    The array is converted into a string and the square brackets are removed
    form it. The resulting string will be the list of frequencies to sweep
    over, organized into comma separated entries.

    Parameters
    ----------
    freq_list: list
                List of frequencies to sweep over

    Returns
    -------
    freq_str: str
              String of comma separated frequencies to be inputted
              into the instrument
    """
    # Convert the frequency list into a string
    freq = str(freq_list)

    # Remove the square brackets from the string of frequencies
    freq_str = freq.split('[')[1].split(']')[0]

    return freq_str
