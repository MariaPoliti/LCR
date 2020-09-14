import csv
import os
import unittest

from LCR import post_processing

# Define example of expected output from instrument
output_signals = [1, 2, 0, 0, 3, 4, 0, 0, 5, 6, 0, 0, 7, 8, 0, 0, 9, 10, 0, 0]
sample = 'molecule'
dist = '1mm'
temp = '20C'
freq_list = [1000, 100, 10, 1, 0.1]


class TestSimulationTools(unittest.TestCase):
    def test_extract_output_signals(self):
        Z_mag, Z_ph = post_processing.extract_output_signals(output_signals)

        assert len(Z_mag + Z_ph) == len(output_signals)/2, \
            ' the data was not correctly extracted'
        assert Z_mag[0] == output_signals[0], \
            ' the data was not correctly extracted'
        assert Z_ph[0] == output_signals[1], \
            ' the data was not correctly extracted'

    def test_get_filename(self):

        filename = post_processing.gen_filename(sample, dist, temp)

        assert isinstance(filename, str), \
            'the filename was not correctly generated'
        assert sample in filename, 'the filename was not correctly generated'

    def test_write_file(self):

        filename = post_processing.gen_filename(sample, dist, temp)
        save_loc = './LCR/tests/'
        post_processing.write_file(
            freq_list, output_signals, filename, save_location=save_loc)
        with open(save_loc + filename + '.csv', mode='r',
                  newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
        assert rows[4][1] == 'frequency',\
            'the file was not correclty saved'
        assert rows[4][2] == 'magnitude',\
            'the file was not correclty saved'
        assert rows[4][3] == 'phase', \
            'the file was not correclty saved'
        os.remove(save_loc + filename + '.csv')
