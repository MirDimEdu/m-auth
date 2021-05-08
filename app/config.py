import os
import asyncio
import yaml
from aiofile import async_open
from types import SimpleNamespace


class YamlConfigManager:
    def __init__(self, interval):
        self._update_interval = interval
        self._config_file = 'config.yaml'
        #self._update_task = asyncio.ensure_future(self._update_loop())

    async def _update_loop(self):
        while True:
            try:
                await self._update()
            except Exception as e:
                print(f'Failed to update config, see you next time \n{repr(e)}')
            await asyncio.sleep(self._update_interval)

    async def _update(self):
        async with async_open(self._config_file, 'r') as f:
            data = yaml.safe_load(await f.read())
#            td = data['server-conf']['port']
#            print(td)
#            if td:
#                cfg.DB_CONNECTION_STRING = int(td)
#            self._config = models.Config.parse_obj(data)

    async def start(self):
        self._update_task = asyncio.ensure_future(self._update_loop())


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


def _get_m_accounts_connection_string(MA_HOST, MA_PORT):
    m_accounts_connection_string = os.getenv('M_ACCOUNTS_CONNECTION_STRING')
    if m_accounts_connection_string:
        return m_accounts_connection_string
    return 'http://{MA_HOST}:{MA_PORT}'


cfg.TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY', 'X-MIRDIMEDU-KEY')
cfg.AUTH_TOKEN_NAME = os.getenv('AUTH_TOKEN_NAME', 'X-MIRDIMEDU-Token')
cfg.TOKEN_EXPIRE_TIME = os.getenv('TOKEN_EXPIRE_TIME', 183)

cfg.HOST = os.getenv('AUTH_HOST', '0.0.0.0')
cfg.PORT = int(os.getenv('AUTH_PORT', '8001'))
cfg.DOMAIN = os.getenv('AUTH_DOMAIN', 'localhost')

cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.STARTUP_DB_ACTION = False

cfg.MA_HOST = os.getenv('M_ACCOUNTS_HOST', '127.0.0.1')
cfg.MA_PORT = int(os.getenv('M_ACCOUNTS_PORT', '8002'))
cfg.MA_ADDR = _get_m_accounts_connection_string(cfg.MA_HOST, cfg.MA_PORT)
