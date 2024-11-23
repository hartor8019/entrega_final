import unittest
from unittest.mock import patch
import pandas as pd
from src.buscar_casos import CasosSearchApp

class TestBuscarCasos(unittest.TestCase):
    def setUp(self):
        self.casos_app = CasosSearchApp("src/casos_base_v3.csv", "src/embeddings.npy")

    def test_missing_data_file(self):
        with self.assertRaises(FileNotFoundError):
            CasosSearchApp("invalid_path.csv", "src/embeddings.npy")

    def test_empty_dataframe(self):
        with patch("src.buscar_casos.pd.read_csv", return_value=pd.DataFrame()):
            app = CasosSearchApp("src/casos_base_v3.csv", "src/embeddings.npy")
            self.assertTrue(app.df.empty)

    def test_valid_columns(self):
        expected_columns = ["Descripcion", "Solucion Propuesta", "Numero de Incidencia"]
        for column in expected_columns:
            self.assertIn(column, self.casos_app.df.columns)

    def test_valid_search(self):
        query = "configurar correo"
        results = self.casos_app.search(query)
        self.assertGreater(len(results), 0)  # Asegúrate de que haya resultados
        self.assertIn("Descripcion", results.columns)
        self.assertIn("similarity", results.columns)

    def test_search_no_results(self):
        query = "query_que_no_existe"
        results = self.casos_app.search(query)
        self.assertEqual(len(results), 0)

    def test_search_invalid_query(self):
        with self.assertRaises(ValueError):
            self.casos_app.search("")

if __name__ == "__main__":
    unittest.main()
