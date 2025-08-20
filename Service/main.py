import config
import grpc_modules
import asyncio

from fastapi import FastAPI
from routers import register_routes


app = FastAPI()

# config.config(app)
register_routes(app)

asyncio.create_task(grpc_modules.start_grpc_server())


@app.get("/mental-connect/algorithm/api/test/hello")
def hello():
    return "Hello! (By FastAPI)"
