import os
from types import SimpleNamespace


cfg = SimpleNamespace()


def _get_m_users_connection_string(MU_HOST, MU_PORT):
    users_connection_string = os.getenv('USERS_CONNECTION_STRING')
    if users_connection_string:
        return users_connection_string
    return 'http://{MU_HOST}:{MU_PORT}'


cfg.TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY', 'X-MIRDIMEDU-KEY')
cfg.AUTH_TOKEN_NAME = os.getenv('AUTH_TOKEN_NAME', 'X-MIRDIMEDU-Token')

cfg.HOST = os.getenv('AUTH_HOST', '0.0.0.0')
cfg.PORT = int(os.getenv('AUTH_PORT', '8000'))

cfg.MU_HOST = os.getenv('M_USERS_HOST', '127.0.0.1')
cfg.MU_PORT = int(os.getenv('M_USERS_PORT', '8008'))
cfg.MU_ADDR = _get_m_users_connection_string(cfg.MU_HOST, cfg.MU_PORT)
