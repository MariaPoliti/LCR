import unittest

from LCR import run
from unittest import mock

# Define example of expected output from instrument
output_signals = [1, 2, 0, 0, 3, 4, 0, 0, 5, 6, 0, 0, 7, 8, 0, 0, 9, 10, 0, 0]
function = ['V', 'I']
amplitude = 0.01

freq_list = [1000, 100, 10, 1]


class TestSimulationTools(unittest.TestCase):
    def test_measurement(self):
        for func in function:
            mocked_instrument = mock.MagicMock()
            mocked_instrument.query_ascii_values.return_value = \
                output_signals

            EIS_measurements = run.measurement(
                mocked_instrument, func, freq_list, amplitude)

            assert mocked_instrument.write.called,\
                'The instrument was not triggered correctly'
            assert mocked_instrument.write.call_count == 18,\
                'Not all commands were correctly sent to the instrument'
            assert EIS_measurements == output_signals, \
                'the instrument did not return the correct output data'
            mocked_instrument.query_ascii_values.assert_called_once_with(
                ':MEM:READ? DBUF')

    def test_cancel_measurement(self):
        mocked_instrument = mock.MagicMock()
        run.cancel_measurement(mocked_instrument)

        mocked_instrument.write.assert_called_once_with(':ABOR')
