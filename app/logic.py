import uuid
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .db import sessions
from .db import _database
from .config import cfg
from . import schemas
from .errors import HTTPabort


async def check_auth(token):
    if token.name != cfg.AUTH_TOKEN_NAME:
        HTTPabort(401, 'Incorrect token name')

    try:
        payload = jwt.decode(token.data, cfg.TOKEN_SECRET_KEY, algorithms=['HS256'])
        user_id: int = payload.get('user_id')
        role: str = payload.get('role')
        session_id = uuid.UUID(payload.get('session_id'))
        expire_time = datetime.fromisoformat(payload.get('expire'))
    except:
        HTTPabort(401, 'Incorrect token data')

    if expire_time < datetime.utcnow():
        query = sessions.delete().where(sessions.c.id == session_id)
        await _database.execute(query)
        HTTPabort(401, 'Token too old')

    query = select(sessions).where(sessions.c.id == session_id)
    cu = await _database.fetch_one(query)
    if not cu:
        HTTPabort(401, 'Unauthorized')


async def new_session(session):
    query = sessions.insert().values(id=session.session_id,
                                     user_id=session.user_id,
                                     client=session.client,
                                     login_time=datetime.utcnow())
    await _database.execute(query)


async def delete_session(session):
    query = sessions.delete().where(sessions.c.id == session.session_id)
    await _database.execute(query)


async def delete_other_sessions(session):
    query = sessions.delete().where(sessions.c.user_id == session.user_id).where(sessions.c.id != session.session_id)
    await _database.execute(query)
