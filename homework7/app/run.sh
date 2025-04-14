set -a
source .env
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind localhost:8000

#python -m uvicorn main:app --reload --env-file .env