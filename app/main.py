import uvicorn

import sys
sys.path.append(".")

# from uvicorn.workers import UvicornWorker
# from gunicorn.app.base import BaseApplication

from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.database.models import Base, db_helper

from app.routes.auth import router as auth_router
from app.routes.rating import router as rate_router
from app.routes.search import router as search_router
from app.routes.user import router as user_router


# class CustomGunicornApp(BaseApplication):
#     def __init__(self, app):
#         self.options = {
#             'bind': '0.0.0.0:8000',
#             'workers': 4,
#             'worker_class': 'uvicorn.workers.UvicornWorker'
#         }
#         self.application = app
#         super().__init__()
#
#     def load_config(self):
#         for key, value in self.options.items():
#             self.cfg.set(key, value)
#
#     def load(self):
#         return self.application


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Trust Not Trust", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(rate_router)
app.include_router(search_router)
app.include_router(user_router)


if __name__ == "__main__":
    # custom_gunicorn_app = CustomGunicornApp(app)
    # custom_gunicorn_app.run()
    uvicorn.run("main:app", reload=True)
