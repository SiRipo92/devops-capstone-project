import unittest
import os
from flask import Flask, jsonify
from flask.testing import FlaskClient
from werkzeug.exceptions import MethodNotAllowed
from service import app
from service.common import status

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"

class TestErrorHandlers(unittest.TestCase):
    # This will be executed before each test case
    def setUp(self):
        """Set up the test client and app context"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """Test the 405 Method Not Allowed error handler"""
        # Simulate a DELETE request to an endpoint that does not support DELETE
        # Assuming you have an endpoint that only supports GET requests
        resp = self.client.delete(BASE_URL) 

        # Assert the response code is 405
        self.assertEqual(resp.status_code, 405)
        
        # Check if the message in the response is correct
        data = resp.get_json()
        self.assertEqual(data['status'], 405)
        self.assertEqual(data['error'], 'Method not Allowed')
        self.assertIn('message', data)
    
    def test_internal_server_error(self):
        """Test the 500 Internal Server Error handler"""
        
        # Create a route that will trigger an exception, simulating a server error
        @app.route('/trigger-500')
        def trigger_500():
            raise Exception("This is a forced internal server error")

        # Make a request to trigger the internal server error
        resp = self.client.get('/trigger-500')

        # Assert the response code is 500
        self.assertEqual(resp.status_code, 500)

        # Check if the message in the response is correct
        data = resp.get_json()
        self.assertEqual(data['status'], 500)
        self.assertEqual(data['error'], 'Internal Server Error')
        # Check for the default error message
        self.assertIn("The server encountered an internal error", data['message'])

if __name__ == '__main__':
    unittest.main()
