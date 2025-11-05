from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.params import Depends
from starlette.responses import JSONResponse
import uvicorn

from database import create_tables
from repository import get_dog_repository, DogRepository
from schemas import Dog


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/dog/{id}")
async def get_a_dog(id: str, dog_repo: DogRepository = Depends(get_dog_repository)) -> Dog:
    response = await dog_repo.get_dog_by_id(id)
    if response is None:
        return JSONResponse(status_code=404, content={"message": "Dog not found"})
    return response


@app.post("/dog")
async def create_dog(dog: Dog, dog_repo: DogRepository = Depends(get_dog_repository)):
    await dog_repo.create_dog(dog)
    return JSONResponse(status_code=201, content={"message": "Dog created successfully"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
