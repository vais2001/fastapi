from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todooo.db")
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class ToDo(Base):
    __tablename__ = 'todo_list'
    id = Column(Integer, primary_key=True)
    task =  Column(String(50))

        
        
  
