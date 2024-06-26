import sys
sys.path.append(".")

from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.database.models import Base, db_helper

from app.routes.auth import router as auth_router
from app.routes.rating import router as rate_router
from app.routes.search import router as search_router
from app.routes.user import router as user_router
from app.routes.admin import router as admin_router


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
app.include_router(admin_router)
