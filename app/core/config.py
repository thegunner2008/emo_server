import os

import sqlalchemy
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

db_name = "postgres"
db_user = "postgres"
db_password = "140fm993"
# host = '/cloudsql/{}'.format("emo-server-380518:us-central1:emo-posgresql")
host = '34.29.12.24:5432'
connection_name = "emo-server-380518:us-central1:emo-posgresql"

url = sqlalchemy.engine.url.URL.create(
    drivername="postgresql+psycopg2",
    username=db_user,
    password=db_password,
    database=db_name,
    query={"host": "{}/{}".format("/cloudsql", connection_name)},
)


class Settings(BaseSettings):
    PROJECT_NAME = 'FASTAPI BASE'
    SECRET_KEY = '123456'
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS = ['*']
    DATABASE_URL = url
    DATABASE_URL_UNIX = 'postgresql+psycopg2://postgres:140fm993@/postgres?unix_sock=/var/lib/postgresql'
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')


settings = Settings()
