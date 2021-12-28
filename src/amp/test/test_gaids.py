import unittest
from unittest import mock
import amp.commands.gaids as gaids


class TestGaids(unittest.TestCase):
    @mock.patch("commands.gaids.api.getAuthenticationHeaders")
    @mock.patch("commands.gaids.requests.get")
    def test_validate(self, mock_input, mock_api):

        mock_input.return_value.status_code = 400

        with self.assertRaises(AssertionError):
            gaids.validate("123456789")

        mock_input.return_value.status_code = 200
        mock_input.return_value.text = '{"is_valid": true}'

        try:
            gaids.validate("GA123456789")
        except AssertionError:
            self.fail("validate() raised AssertionError unexpectedly!")
