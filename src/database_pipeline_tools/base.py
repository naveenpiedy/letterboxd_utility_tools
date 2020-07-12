from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://admin:admin@localhost/letterboxd_movies")
# engine = create_engine('sqlite:///letterboxd_movies.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
