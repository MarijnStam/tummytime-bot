from sqlmodel import SQLModel, Session, create_engine, engine
from typing import List
from datetime import datetime as time 

from models import *

db_file_name = "TummyTime.sqlite3"
sqlite_url = f"sqlite:///{db_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

def feel_entry(feel: int, symptoms: List['str']) -> Feel:
    with Session(engine) as session:
        db_feel = Feel(id=None, feel=feel, timestamp=timestamp())
        session.add(db_feel)
        session.commit()
        session.refresh(db_feel)
        return db_feel
    
def timestamp():
    return time.now().strftime("%d/%m/%Y %H:%M:%S")