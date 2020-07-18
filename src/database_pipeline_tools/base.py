import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os.path import join
from dotenv import load_dotenv

dotenv_path = join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

engine = create_engine(os.environ.get("db_conn"))
Session = sessionmaker(bind=engine)
Base = declarative_base()
