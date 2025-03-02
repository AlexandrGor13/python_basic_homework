from fastapi import FastAPI, status
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    '/ping',
    status_code=status.HTTP_200_OK
)
def pong():
    return {"message": "pong"}


# if __name__ == '__main__':
#     uvicorn.run("main:app", reload=True)
