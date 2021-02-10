# Music Genre recognition

## Installing
Install dependencies with:

```pip install -r requirements.txt```

## Run

docker build -t genre-recognition . && docker run -d -p 8080:80 genre-recognition

### Development
Start app with:

```uvicorn main:app --reload```

(Ctrl+C to quit)

App will start at:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc


Project based on tiangolo/full-stack-fastapi-postgresql

```About
Full stack, modern web application generator. 
Using FastAPI, PostgreSQL as database, Docker, automatic HTTPS and more.```