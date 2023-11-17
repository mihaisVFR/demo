from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
import json
Base = declarative_base()
engine = create_engine('sqlite:///adm_demo.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_status = Column(String(32), unique=True, nullable=False)
    user_login = Column(String(32), unique=True, nullable=False)
    hash_password = Column(String(128), nullable=False)


# class Variables(Base):
#     __tablename__ = "variables"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(32))
#     value = Column(String)
#     description = Column(String, nullable=True)


class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    account = Column(String, unique=True)


def create_tables():
    Base.metadata.create_all(engine)


def from_json_to_db():
    with open('treeviewdata.json', encoding="utf-8") as f:
        tree = json.load(f)
        for i in tree:
             entryName = Clients(name =i["name"], account =i["purpose"])
             session.add(entryName)
        session.commit()


# def add_variables(name, value, description):
#     var = Variables(name=name, value=value, description=description)
#     session.add(var)
#     session.commit()


def delete():
    session.query(Clients).delete()
    session.commit()

#add_variables("day_state", True, )

day_state = True
receipt_number =1
# password = str(pwd_context.hash("123456"))
# print(pwd_context.verify("123456",password))
