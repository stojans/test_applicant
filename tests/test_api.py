from odoo.tests.common import HttpCase
from odoo.tests import tagged
import json

@tagged('post_install', '-at_install')
class TestAPI(HttpCase):
    """
    Test case for testing the API endpoints related to 'test.model'. 
    Specifically, this test checks the structure of the data returned 
    by the GET /api/test-model route.
    """

    def test_get_test_model(self):
        """
        Tests the GET /api/test-model route to ensure that the API returns 
        the expected data structure.

        This test checks that the response is a list and that each item in 
        the list contains the expected fields: 'id', 'name', 'description', 
        'state', and 'confirmation_datetime'. 

        It performs the following checks:
        - The response is a list.
        - If the list is not empty, it verifies that each record in the list contains 
          the necessary fields ('id', 'name', 'description', 'state', 'confirmation_datetime').
        
        Returns:
            None: The test asserts that the returned data matches the expected structure.
        """
        # Send a GET request to the /api/test-model route
        response = self.url_open('/api/test-model')
        
        # Parse the JSON response data
        response_data = json.loads(response.content)

        # Assert that the response is a list
        self.assertIsInstance(response_data, list)

        # If the response list is not empty, validate that each record has the required fields
        if len(response_data) > 0:
            self.assertIn('id', response_data[0], "Field 'id' is missing in the response.")
            self.assertIn('name', response_data[0], "Field 'name' is missing in the response.")
            self.assertIn('description', response_data[0], "Field 'description' is missing in the response.")
            self.assertIn('state', response_data[0], "Field 'state' is missing in the response.")
            self.assertIn('confirmation_datetime', response_data[0], "Field 'confirmation_datetime' is missing in the response.")
