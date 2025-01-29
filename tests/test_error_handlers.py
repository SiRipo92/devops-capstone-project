import unittest
import os
from flask import abort
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"


# Define the route only once using Flask's `before_first_request`
@app.route("/trigger-500")
def trigger_500():
    abort(500)


class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        """Set up the test client"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """Test the 405 Method Not Allowed error handler"""
        resp = self.client.delete(BASE_URL)

        # Assert the response code is 405
        self.assertEqual(resp.status_code, 405)

        # Check if the message in the response is correct
        data = resp.get_json()
        self.assertEqual(data["status"], 405)
        self.assertEqual(data["error"], "Method not Allowed")
        self.assertIn("message", data)

    def test_internal_server_error(self):
        """Test the 500 Internal Server Error handler"""
        resp = self.client.get("/trigger-500")

        # Assert the response code is 500
        self.assertEqual(resp.status_code, 500)

        # Check if the message in the response is correct
        data = resp.get_json()
        self.assertEqual(data["status"], 500)
        self.assertEqual(data["error"], "Internal Server Error")
        self.assertIn("The server encountered an internal error", data["message"])


if __name__ == "__main__":
    unittest.main()
