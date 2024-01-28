import uvicorn

import sys
sys.path.append(".")

from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.database.models import Base, db_helper

from app.routes.auth import router as auth_router
# from routers.rate import router as rate_router
# from routers.search import router as search_router
from app.routes.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Trust Not Trust", lifespan=lifespan)


app.include_router(auth_router)
# app.include_router(rate_router)
# app.include_router(search_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
