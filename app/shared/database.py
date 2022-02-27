from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..constants.database import mysqlDomain, mysqlPort, mysqlDatabase, mysqlUser, mysqlPassword

SQLALCHEMY_DATABASE_URL = f'mysql://{mysqlUser}:{mysqlPassword}@{mysqlDomain}:{mysqlPort}/{mysqlDatabase}'

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
