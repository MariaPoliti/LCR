import unittest

from LCR import corrections
from unittest import mock

# Define example of expected output from instrument


class TestSimulationTools(unittest.TestCase):
    def test_cable_length(self):
        mocked_instrument = mock.MagicMock()
        n = 1
        corrections.cable_length(mocked_instrument, length=n)

        assert mocked_instrument.write.called,\
            'The instrument was not triggered correctly'
        assert mocked_instrument.write.call_count == 5,\
            'Not all commands were correctly sent to the instrument'
        mocked_instrument.write.assert_called_with(':CORR:LENG ', n)

    def test_open(self):
        mode = ['ON', 'OFF']
        for m in mode:
            mocked_instrument = mock.MagicMock()
            corrections.open(mocked_instrument, mode=m, collect=False)
            assert mocked_instrument.write.called,\
                'The instrument was not triggered correctly'
            assert mocked_instrument.write.call_count == 5,\
                'Not all commands were correctly sent to the instrument'
            mocked_instrument.write.assert_called_with(':CORR:OPEN:STAT '+m)

        mocked_instrument = mock.MagicMock()
        corrections.open(mocked_instrument, mode='ON', collect=True)
        mocked_instrument.write.assert_called_with(':CORR:OPEN:EXEC')

    def test_short(self):
        mode = ['ON', 'OFF']
        for m in mode:
            mocked_instrument = mock.MagicMock()
            corrections.short(mocked_instrument, mode=m, collect=False)

            assert mocked_instrument.write.called,\
                'The instrument was not triggered correctly'
            assert mocked_instrument.write.call_count == 5,\
                'Not all commands were correctly sent to the instrument'
            mocked_instrument.write.assert_called_with(':CORR:SHOR:STAT '+m)

        mocked_instrument = mock.MagicMock()
        corrections.short(mocked_instrument, mode='ON', collect=True)
        mocked_instrument.write.assert_called_with(':CORR:SHOR:EXEC')
