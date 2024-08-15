import uvicorn
from fastapi import FastAPI

from app.router import router as channel_routers

app = FastAPI()

app.include_router(channel_routers)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
