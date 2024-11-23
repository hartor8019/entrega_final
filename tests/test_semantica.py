import unittest
from src.semantica import SemanticSearch

class TestSemanticSearch(unittest.TestCase):
    def setUp(self):
        # Inicializa el modelo para pruebas
        self.semantic_search = SemanticSearch()

    def test_encode_data(self):
        data = ["Prueba uno", "Prueba dos"]
        embeddings = self.semantic_search.encode_data(data)
        self.assertEqual(len(embeddings), 2)

    def test_find_similarities(self):
        data = ["Prueba uno", "Prueba dos"]
        embeddings = self.semantic_search.encode_data(data)
        similarities = self.semantic_search.find_similarities("Prueba uno", embeddings)
        self.assertEqual(len(similarities), len(data))

if __name__ == "__main__":
    unittest.main()
