
```
// Tạo postgresql Databases via CLI (Ubuntu 20.04)
$ sudo -u postgres psql
# CREATE DATABASE fastapi_base;
# CREATE USER db_user WITH PASSWORD 'secret123';
# GRANT ALL PRIVILEGES ON DATABASE fastapi_base TO db_user;

// Clone project & run
$ cd fastapi-base
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cp env.example .env       // Recheck SQL_DATABASE_URL ở bước này
$ alembic upgrade head
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```