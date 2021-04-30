from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from typing import Optional

from . import schemas
from . import logic
from .config import cfg


router = APIRouter()


def HTTPanswer(status_code, description):
    return JSONResponse(
        status_code=status_code,
        content={'content': description},
    )


@router.post('/is_auth')
async def is_auth(token: schemas.Token):
    await logic.check_auth(token)
    return HTTPanswer(200, 'Auth OK')


@router.post('/new_session')
async def new_session(session: schemas.Session):
    await logic.new_session(session)
    return HTTPanswer(201, 'Added')


@router.delete('/delete_session')
async def delete_session(session: schemas.Session):
    await logic.delete_session(session)
    return HTTPanswer(200, 'Deleted')


@router.delete('/delete_other_sessions')
async def delete_other_sessions(session: schemas.Session):
    await logic.delete_other_sessions(session)
    return HTTPanswer(200, 'Deleted')
