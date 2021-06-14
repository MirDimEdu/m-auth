import uuid
import databases

from sqlalchemy import (create_engine, Table, Column, Integer, String, DateTime, MetaData,
                        ForeignKey)
from sqlalchemy.dialects.postgresql import UUID, TEXT
from datetime import datetime

from .config import cfg


_database = databases.Database(cfg.DB_CONNECTION_STRING) #, ssl=True)
_engine = create_engine(cfg.DB_CONNECTION_STRING)
_metadata = MetaData()


sessions = Table('sessions', _metadata,
    Column('id', UUID, default=uuid.uuid4, primary_key=True),
    Column('account_id', Integer, nullable=False),
    Column('client', String, nullable=False),
    Column('login_time', DateTime, default=datetime.utcnow, nullable=False)
)


def create_tables():
    print('Dropping existing tables', end='', flush=True)
    try:
        _metadata.reflect(_engine)
        _metadata.drop_all(_engine)
        print(' - OK')
    except Exception as e:
        print(f'Failed to drop tables.\n{str(e)}')
    print('Creating tables', end='', flush=True)
    _metadata.create_all(_engine)
    print(' - OK')
