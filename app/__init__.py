from fastapi import FastAPI

from .router import router
from . import logic
from .config import cfg
from .errors import exception_handlers


app = FastAPI(exception_handlers=exception_handlers)

app.include_router(router)
