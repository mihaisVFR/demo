from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context

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


class Variables(Base):
    __tablename__ = "variables"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    value = Column(String)
    description = Column(String, nullable=True)

#Base.metadata.create_all(engine)

# entryName = User(user_status="Инкассатор", user_login="2222", hash_password = pwd_context.hash("654321") )
# # Чтобы сохранить наш объект ClassName, мы добавляем его в наш сессию:
# session.add(entryName)
# session.commit()

password = str(pwd_context.hash("123456"))
print(pwd_context.verify("123456",password))
