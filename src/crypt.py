#from passlib.context import CryptContext

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#ashed_password = pwd_context.hash("lcampo")
#print(hashed_password)

from main import df
from main import similarities

print("Número de filas en df:", len(df))
print("Número de valores en similarities:", len(similarities))