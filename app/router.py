from fastapi import APIRouter, Depends, Header, Response
from fastapi.responses import JSONResponse
from typing import Optional

from . import schemas
from . import logic
from .config import cfg


router = APIRouter()


@router.post('/is_auth', response_model=schemas.CurrentUser)
async def is_auth(token: schemas.Token):
    return await logic.check_auth(token)
