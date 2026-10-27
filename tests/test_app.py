"""Simple smoke tests. Run with: python -m unittest discover -s tests"""
import unittest
import app as student_app

class DashboardTests(unittest.TestCase):
    def setUp(self):
        student_app.app.config['TESTING'] = True
        self.client = student_app.app.test_client()

    def test_dashboard_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Analytics Dashboard', response.data)

    def test_api_returns_students(self):
        response = self.client.get('/api/students')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertGreater(len(response.get_json()), 0)

if __name__ == '__main__':
    unittest.main()
