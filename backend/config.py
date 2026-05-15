"""
FinancePro Backend Configuration
Configurações do sistema
"""
import os
from datetime import timedelta

class Config:
    """Configurações da aplicação"""
    
    # Secret Key para JWT
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'financepro-super-secret-key-2024'
    
    # Configurações JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Configurações do Banco de Dados MySQL
    DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Jhon2008',
    'database': 'financepro',
    'charset': 'utf8mb4',
    'autocommit': True,
    'raise_on_warnings': True
}
    
    # Configurações de Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # Timezone
    TIMEZONE = 'America/Sao_Paulo'
    
    # Paginação
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    TESTING = False

# Configuração ativa
config = DevelopmentConfig()