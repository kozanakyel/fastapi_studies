from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

database = os.getenv("DATABASE")

SQLALCHEMY_DATABASE_URL = database

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""

db = os.getenv("DB")
host = os.getenv("HOST")
password = os.getenv("PSWD")
userDB = os.getenv("USER")

while True:    
    try:
        conn = psycopg2.connect(host=host, database=db, 
                            user=userDB, password=password, 
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successfull')
        break
    except Exception as error:
        print("connetcion failedd error--------------")
        print('Error:', error)
        time.sleep(2)


"""
