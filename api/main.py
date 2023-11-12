from fastapi import FastAPI
import logger
from swarms import api as swarms_api
from generations import api as generations_api


app = FastAPI()

# Include router
app.include_router(swarms_api.api_router)
app.include_router(generations_api.api_router)


@app.get("/ping")
async def read_root():
    return {"status": "ok"}
