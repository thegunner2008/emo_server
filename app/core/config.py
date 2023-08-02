import os

import sqlalchemy
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

db_name = "emodb"
db_user = "huy"
db_password = "123456"
host = 'localhost'
connection_name = "emo-server-380518:us-central1:emo-posgresql"

url = sqlalchemy.engine.url.URL.create(
    drivername="postgresql+psycopg2",
    username=db_user,
    password=db_password,
    database=db_name,
    # host=host,
    query={"host": "{}/{}".format("/cloudsql", connection_name)},
)

url1 = f'postgresql+psycopg2://{db_user}:{db_password}@{host}/{db_name}'


class Settings(BaseSettings):
    PROJECT_NAME = 'FASTAPI BASE'
    SECRET_KEY = '123456'
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS = ['*']
    DATABASE_URL = url1
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')


settings = Settings()
