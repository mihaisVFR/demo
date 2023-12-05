from sqlalchemy import Column, Integer, String, ForeignKey  # Table
from sqlalchemy.orm import relationship  # backref
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
#  from sqlalchemy import MetaData
import json


Base = declarative_base()
engine = create_engine('sqlite:///adm_demo.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):

    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_status = Column(String(32), nullable=False)
    user_login = Column(String(32), unique=True, nullable=False)
    hash_password = Column(String(128), nullable=False)
    client = relationship("Clients", backref="client")

    def __init__(self, user_status, user_login, hash_password):
        self.user_login = user_login
        self.hash_password = hash_password
        self.user_status = user_status

    def to_dict(self):
        desearialaze = {
            "login": self.user_login,
            "password": self.hash_password,
            "status": self.user_status
        }
        return desearialaze


class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    account = Column(String, unique=True)
    user_login = Column(Integer, ForeignKey('user.user_login'))

    def __init__(self, name, account, user_login):
        self.name = name
        self.account = account
        self.user_login = user_login

    def to_dict(self):
        desearialaze = {
            "name": self.name,
            "purpose": self.account
        }
        return desearialaze


def create_tables():
    Base.metadata.create_all(engine)


def from_json_to_db():
    with open('treeviewdata.json', encoding="utf-8") as f:
        tree = json.load(f)
        for i in tree:
            entry_name = Clients(name=i["name"], account=i["purpose"], user_login="1111")
            session.add(entry_name)
        session.commit()


def delete_tables():
    User.__table__.drop(engine)
    Clients.__table__.drop(engine)


def delete_table_data():
    session.query(Clients).delete()
    session.commit()


def get_clients():
    data = session.query(Clients).all()
    list_of_dict = []
    for row in data:
        list_of_dict.append(row.to_dict())
    return list_of_dict


def get_user(user_login):
    data = session.query(User).filter_by(user_login=user_login).first()
    if data is not None:
        return data


def add_user(user_status, name, password):
    ent = User(user_status=user_status, user_login=name, hash_password=pwd_context.hash(password))
    session.add(ent)
    session.commit()


def add_users():
    add_user("Кассир", "1111", "1111")
    add_user("Инкассатор", "2222", "2222")
    add_user("Кассир", "3333", "123456")
    add_user("Об авторах", "911", "119")


def add_clients():
    add_client("ООО Дионис", "40702810020202020202", "1111")
    add_client("ООО Солар", "40702810030303030303", "1111")
    add_client("ИП Иванов", "40802810010203040506", "1111")
    add_client("ИП Бокарев", "40802810123321098890", "3333")

def add_client(name, account, user_login):
    ent = Clients(name=name, account=account, user_login=user_login)
    session.add(ent)
    session.commit()


def refill_db():
    delete_tables()
    create_tables()
    add_users()
    # from_json_to_db()
    add_clients()
