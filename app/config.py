import os
from types import SimpleNamespace


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


cfg.TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY', 'X-MIRDIMEDU-KEY')
cfg.AUTH_TOKEN_NAME = os.getenv('AUTH_TOKEN_NAME', 'X-MIRDIMEDU-Token')

cfg.HOST = os.getenv('AUTH_HOST', '0.0.0.0')
cfg.PORT = int(os.getenv('AUTH_PORT', '8000'))

cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.STARTUP_DB_ACTION = False
