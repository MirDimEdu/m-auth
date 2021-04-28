import uuid
import httpx
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

from .config import cfg
from . import schemas
from .errors import HTTPabort


async def check_auth(token):
    if token.name != cfg.AUTH_TOKEN_NAME:
        HTTPabort(401, 'Incorrect token name')

    try:
        payload = jwt.decode(token.data, cfg.TOKEN_SECRET_KEY, algorithms=['HS256'])
        user_id: int = payload.get('user_id')
        token_id = uuid.UUID(payload.get('token_id'))
        expire_time = datetime.fromisoformat(payload.get('expire'))
    except:
        HTTPabort(401, 'Incorrect token data')

    if expire_time < datetime.utcnow():
        async with httpx.AsyncClient() as ac:
            json = {'t_id': token_id}
            answer = await ac.delete(f'{cfg.MU_ADDR}/auth/delete_token', json=json)
            HTTPabort(401, 'Token too old')

    async with httpx.AsyncClient() as ac:
        json={'user_id': user_id, 'token_id': token_id}  
        answer = await ac.post(f'{cfg.MU_ADDR}/auth/me', json=json)

        if answer.status_code != 200:
            HTTPabort(401, 'Unauthorized')
        return schemas.CurrentUser(**answer.json())
