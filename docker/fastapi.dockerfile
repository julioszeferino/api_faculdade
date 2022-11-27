FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
LABEL maintainer="Julio Zeferino <julioszeferino@gmail.com>"
WORKDIR /app
COPY . /app/
RUN cd /app && pip install --upgrade pip setuptools wheel 
RUN cd /app && pip install --no-cache-dir --upgrade -r requirements.txt && rm requirements.txt 
EXPOSE 8000
ENTRYPOINT cd /app && alembic upgrade head && python main.py
