import uvicorn

from app import app
from app.config import cfg


if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config['formatters']['access']['fmt'] = '%(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s'

    uvicorn.run(
        'main:app',
        host=cfg.HOST,
        port=cfg.PORT,
        log_config=log_config,
        reload=False
    )
