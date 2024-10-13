import os

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_DOMAIN')

url = f'mysql+mysqlconnector://{db_user}:{db_password}@{host}/{db_name}'


class Settings(BaseSettings):
    PROJECT_NAME = 'FASTAPI EMO'
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS = ['*']
    DATABASE_URL = url
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')


settings = Settings()
