import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import Session
from typing import Generator

from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
if (os.getenv("ENVIRONMENT") == "DOCKER"):
    MYSQL_HOST = os.getenv('MYSQL_HOST')
else:
    MYSQL_HOST = "127.0.0.1"

MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


engine = create_engine(
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine) )
Base = declarative_base()

def get_db_session() -> Generator[Session, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()

def start_db():
    retries = 10
    delay = 3

    for i in range(retries):
        try:
            print("Attempting to connect to the database...")
            Base.metadata.create_all(engine)
            print("Database connected and tables created.")
            break
        except OperationalError as e:
            print(f"Database connection failed ({i + 1}/{retries}). Retrying in {delay}s...")
            time.sleep(delay)
    else:
        print("Failed to connect to the database after several retries.")
        raise