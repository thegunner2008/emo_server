FROM python:3.9.2

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN groupadd -g 1000 app_group

RUN useradd -g app_group --uid 1000 app_user

RUN chown -R app_user:app_group /app

USER app_user

CMD exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]