import unittest
from fastapi.testclient import TestClient
from src.main import app

class TestMainAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_protected_routes(self):
        # Simula una solicitud sin cookies
        response = self.client.get("/")
        self.assertEqual(response.status_code, 307)  # Verifica redirección a /login
        self.assertEqual(response.headers["location"], "/login")  # Verifica la URL de redirección

    def test_search_with_special_characters(self):
        response = self.client.post("/search", json={"query": "!@#$%^&*()"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())

    def test_middleware_unauthenticated_redirect(self):
        response = self.client.get("/", cookies={})
        self.assertEqual(response.status_code, 307)
        #self.assertEqual(response.headers["location"], "/login")

    def test_middleware_authenticated_access(self):
        response = self.client.get("/", cookies={"session_token": "valid_token"})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()