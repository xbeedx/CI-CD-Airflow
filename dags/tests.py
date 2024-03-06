import unittest
from unittest.mock import patch, MagicMock
from plugin.getProfile import * 
from plugin.getRating import *

class TestGetProfileOperator(unittest.TestCase):

    @patch('requests.get')
    def test_execute(self, mock_get):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.json.return_value = {'profile': 'test'}

        # Make the mock get function return the mock response
        mock_get.return_value = mock_response

        # Create an instance of GetProfileOperator
        operator = GetProfileOperator(task_id='test_task')

        # Call the execute method and check the result
        result = operator.execute(context={})

        # Check that the requests.get function was called with the correct arguments
        mock_get.assert_called_with('https://financialmodelingprep.com/api/v3/company/profile/AAPL', params={'apikey': 'b5c4e8d0b3f2e3c1b0e8c2f3b0e8c2f3'})

        # Check that the result is as expected
        self.assertIn('timestamp', result)
        self.assertEqual(result['profile'], {'profile': 'test'})

class TestGetRatingOperator(unittest.TestCase):
    
        @patch('requests.get')
        def test_execute(self, mock_get):
            # Create a mock response object
            mock_response = MagicMock()
            mock_response.json.return_value = {'Rating': 'test'}
    
            # Make the mock get function return the mock response
            mock_get.return_value = mock_response
    
            # Create an instance of GetRatingOperator
            operator = GetRatingOperator(task_id='test_task')
    
            # Call the execute method and check the result
            result = operator.execute(context={})
    
            # Check that the requests.get function was called with the correct arguments
            mock_get.assert_called_with('https://financialmodelingprep.com/api/v3/company/Rating/AAPL', params={'apikey': 'b5c4e8d0b3f2e3c1b0e8c2f3b0e8c2f3'})
    
            # Check that the result is as expected
            self.assertIn('timestamp', result)
            self.assertEqual(result['Rating'], {'Rating': 'test'})

if __name__ == '__main__':
    unittest.main()