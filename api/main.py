from fastapi import FastAPI
import logger
from swarms import api as swarms_api
from projects import api as projects_api
from tasks import api as tasks_api



app = FastAPI()

# Include router
app.include_router(swarms_api.api_router)
app.include_router(projects_api.api_router)
app.include_router(tasks_api.api_router)


@app.get("/ping")
async def read_root():
    return {"status": "ok"}
