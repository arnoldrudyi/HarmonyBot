import os

import sqlalchemy as sql
import sqlalchemy.orm as orm


def sqlalchemy_database_uri():
    return f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}" \
           f"@localhost/{os.getenv('POSTGRES_DB')}"


engine = sql.create_engine(sqlalchemy_database_uri())
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = orm.declarative_base()
