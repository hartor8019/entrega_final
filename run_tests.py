import unittest
import sys
import os

# Agrega src y tests al PYTHONPATH
sys.path.append(os.path.abspath('src'))
sys.path.append(os.path.abspath('tests'))

# Descubre y ejecuta las pruebas
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)
