import unittest
import os
from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        # Crea un archivo CSV temporal para pruebas
        self.file_path = "test_data.csv"
        with open(self.file_path, "w") as f:
            f.write("Nombre usuario,Departamento\nJohn Doe,IT\nJane Smith,HR")

    def tearDown(self):
        # Elimina el archivo temporal después de cada prueba
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def load_data(self):
        try:
            return pd.read_csv(self.file_path)
        except pd.errors.ParserError:
         raise ValueError("El archivo tiene un formato inválido.")

    def test_load_data_success(self):
        # Prueba que el archivo se cargue correctamente
        loader = DataLoader(self.file_path)
        df = loader.load_data()
        self.assertEqual(len(df), 2)  # Verifica que haya 2 filas
        self.assertIn("Nombre usuario", df.columns)  # Verifica que exista la columna 'Nombre usuario'
        self.assertIn("Departamento", df.columns)  # Verifica que exista la columna 'Departamento'

    def test_file_not_found(self):
        # Prueba el manejo de archivos inexistentes
        loader = DataLoader("non_existent_file.csv")
        df = loader.load_data()
        self.assertTrue(df.empty)  # Verifica que el DataFrame esté vacío

    def test_load_data_with_different_delimiter(self):
        file_path = "test_data_with_tabs.csv"
        with open(file_path, "w") as f:
            f.write("Nombre\tDepartamento\nJohn Doe\tIT\nJane Smith\tHR")
        loader = DataLoader(file_path)
        df = loader.load_data()
        self.assertFalse(df.empty)
        os.remove(file_path)

    def test_load_data_with_invalid_format(self):
        loader = DataLoader("corrupted_file.csv")
        with self.assertRaises(ValueError):
            loader.load_data()
            
if __name__ == "__main__":
    unittest.main()
