from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import MetaData
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

    def __init__(self, user_login, hash_password):
        self.user_login = user_login
        self.hash_password = hash_password

    def to_dict(self):
        desearialaze = {"login": self.user_login, "password": self.hash_password}
        return desearialaze


class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    account = Column(String, unique=True)

    def __init__(self, name, account):
        self.name = name
        self.account = account

    def to_dict(self):
        desearialaze = {"name": self.name, "purpose": self.account}
        return desearialaze

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

def delete_table(class_name):
    class_name.__table__.drop(engine)


def delete_table_data():
    session.query(Clients).delete()
    session.commit()

#add_variables("day_state", True, )
# password = str(pwd_context.hash("123456"))
# print(pwd_context.verify("123456",password))

# data = session.query(Clients).all()
# for row in data:
#     print(row.to_dict())

def get_clients():
    data = session.query(Clients).all()
    list_of_dict = []
    for row in data:
        list_of_dict.append(row.to_dict())
    return(list_of_dict)


def get_user(user_login):
    data = session.query(User).filter_by(user_login=user_login).first()
    if data is not None:
        return data.to_dict()
