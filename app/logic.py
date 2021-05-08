import uuid
import httpx
from fastapi import Request
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .db import sessions
from .db import _database
from .config import cfg
from . import schemas # maybe fix to from .schemas import CurrenUser
from .errors import HTTPabort


async def auth_required(request: Request):
    token = request.cookies.get(cfg.AUTH_TOKEN_NAME)
    if not token:
        HTTPabort(401, 'Incorrect token name')

    try:
        payload = jwt.decode(token, cfg.TOKEN_SECRET_KEY, algorithms=['HS256'])
        account_id: int = payload.get('account_id')
        role: str = payload.get('role')
        session_id = uuid.UUID(payload.get('session_id'))
        login_time = datetime.fromisoformat(payload.get('login_time'))
        client = payload.get('client')
    except:
        HTTPabort(401, 'Incorrect token data')

    if datetime.utcnow() > (login_time + timedelta(days=cfg.TOKEN_EXPIRE_TIME)):
        query = sessions.delete().where(sessions.c.id == session_id)
        await _database.execute(query)
        HTTPabort(401, 'Token too old')

    query = select(sessions).where(sessions.c.id == session_id)
    current_user = await _database.fetch_one(query)
    if not current_user:
        HTTPabort(401, 'Unauthorized')

    return schemas.CurrentUser(cu, role)


async def authenticate_user(login, password):
    async with httpx.AsyncClient() as ac:
        json = {
            'login': login,
            'password': password
        }
        answer = await ac.post(f'{cfg.MA_ADDR}/verify_account', json=json)

        if answer.status_code != 200:
            HTTPabort(answer.status_code, answer.json()['content'])
        account_id = answer.json()['account_id']
        role = answer.json()['role']


    session_id = uuid.uuid4()
    query = sessions.insert().values(id=session_id,
                                     account_id=account_id,
                                     client='web',
                                     login_time=datetime.utcnow())
    await _database.execute(query)

    jwt_account_data = {
        'account_id': account_id,
        'role': role,
        'session_id': str(session_id),
        'client': 'web',
        'login_time': datetime.utcnow().isoformat()
    }

    return jwt.encode(jwt_account_data, cfg.SECRET_KEY, algorithm='HS256')


async def logout_user(session_id):
    query = sessions.delete().where(sessions.c.id == session_id)
    await _database.execute(query)


async def close_other_sessions(current_user, password):
    async with httpx.AsyncClient() as ac:
        json = {
            'account_id': current_user.account_id,
            'password': password
        }
        answer = await ac.post(f'{cfg.MA_ADDR}/verify_account', json=json)

        if answer.status_code != 200:
            HTTPabort(answer.status_code, answer.json()['content'])

    query = sessions.delete().where(sessions.c.account_id == current_user.account_id).where(sessions.c.id != current_user.session_id)
    await _database.execute(query)


async def delete_sessions(session, which=None):
    query = sessions.delete().where(sessions.c.account_id == session.account_id)
    if which == 'other':
        query = query.where(sessions.c.id != session.session_id)
    await _database.execute(query)
