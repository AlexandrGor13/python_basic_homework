## Данный проект представляет собой web-приложение с использованием FastAPI и Dockerfile для создания образа в docker.

## Управление зависимостями осуществляется через Poetry

Для создания образа необходимо выполнить команду 
```
docker build -t my-app .
```

Для создания и запуска контейнера необходимо выполнить команду
```
docker run -d --name my-app-conteiner -p 8000:8000 my-app
```

После этого контейнер запускается с портом 8000 (http://127.0.0.1:8000/)
```
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                    NAMES
ae3d25f93048   my-app    "poetry run fastapi …"   1 minutes ago   Up 1 minutes   0.0.0.0:8000->8000/tcp   my-app-conteiner

```

