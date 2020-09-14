import unittest

from LCR import frequency

high_freq = 100
low_freq = 1
points = 10


class TestSimulationTools(unittest.TestCase):
    def test_freq_list(self):

        freq_list = frequency.freq_list(
            high_freq, low_freq, pts_per_decade=points)
        assert freq_list[0] == high_freq, \
            'The high frequency point is not correct'
        assert freq_list[-1] == low_freq,\
            'The low frequency point is not correct'
        assert isinstance(freq_list, list), \
            'the output of is not a list'

    def test_freq_str(self):
        freq_list = frequency.freq_list(
            high_freq, low_freq, pts_per_decade=points)
        freq_str = frequency.freq_str(freq_list)

        assert isinstance(freq_str, str),\
            ' the output is not a string'
