import os
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


# host = '/cloudsql/{}'.format("emo-server-380518:us-central1:emo-posgresql")
class Settings(BaseSettings):
    PROJECT_NAME = 'FASTAPI BASE'
    SECRET_KEY = '123456'
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS = ['*']
    DATABASE_URL = 'postgresql+psycopg2://postgres:140fm993@10.82.84.3:5432/postgres'
    DATABASE_URL_UNIX = 'postgresql+psycopg2://postgres:140fm993@/postgres?unix_sock=/var/lib/postgresql'
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')


settings = Settings()
