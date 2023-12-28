from fastapi import FastAPI

from app.database.create_tables import create_tables

from app.routers.code import router as code_router
from app.routers.edit import router as edit_router
from app.routers.rate import router as rate_router
from app.routers.search import router as search_router
from app.routers.user import router as user_router


app = FastAPI(title="Trust Not Trust")

create_tables()

app.include_router(code_router)
app.include_router(edit_router)
app.include_router(rate_router)
app.include_router(search_router)
app.include_router(user_router)
