@REM uvicorn main:app --host 0.0.0.0 --port 10000
@REM pip freeze > requirements.txt 
@REM docker build -t steam_api .
@REM docker run -p 80:80 steam_api
docker compose up
