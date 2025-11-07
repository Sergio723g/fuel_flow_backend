import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de la base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'fuelflow')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Configuración de autenticación
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    @property
    def DATABASE_URL(self):
        return f"dbname={self.DB_NAME} user={self.DB_USER} password={self.DB_PASSWORD} host={self.DB_HOST} port={self.DB_PORT}"







