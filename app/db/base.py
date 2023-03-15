from typing import Generator
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes


def getconn():
    # if env var PRIVATE_IP is set to True, use private IP Cloud SQL connections
    # ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") is True else IPTypes.PUBLIC
    # if env var DB_IAM_USER is set, use IAM database authentication
    # user, enable_iam_auth = (
    #     (os.getenv("DB_IAM_USER"), True)
    #     if os.getenv("DB_IAM_USER")
    #     else (os.getenv("DB_USER"), False)
    # )
    # initialize Cloud SQL Python connector object
    with Connector(ip_type=IPTypes.PUBLIC) as connector:
        conn = connector.connect(
            "emo-server-380518:us-central1:emo-posgresql",
            "pg8000",
            user="postgres",
            password="140fm993",
            db="postgres",
        )
        return conn


SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn)
# engine = create_engine(settings.DATABASE_URL_UNIX, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
