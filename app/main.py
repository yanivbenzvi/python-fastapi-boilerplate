from fastapi import FastAPI
from app.utils.log_manager import init_loggers
from app.middleware.middlewares_manager import init_middlewares
from app.schedule_tasks import init_schedule_tasks

app = FastAPI()
init_loggers(app)

trustApiEndpoints = FastAPI(root_path="/api/v1")
init_middlewares(app)
init_schedule_tasks(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
