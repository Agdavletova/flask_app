import datetime

from sqlalchemy import create_engine, Integer, String, DateTime, func, ForeignKey, event
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

from werkzeug.security import generate_password_hash

POSTGRES_USER=os.getenv("POSTGRES_USER", "test_user")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "1234user")
POSTGRES_DB=os.getenv("POSTGRES_DB", "test_user_database")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
          f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
class User(Base):
    '''Класс пользователей'''
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    advertisements = relationship("Advertisement", back_populates="owner")

    def set_password(self, password: str):
        '''Установка захешированного пароля'''
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    @property
    def dict(self):
        return {
            "id":self.id,
            "username":self.username,
            "email":self.email
        }

@event.listens_for(User, "before_insert")
def hash_user_password(mapper, connection, target: User):
    '''Хеширование пароля перед добавлением в бд'''
    if target.password:
        target.set_password(target.password)

class Advertisement(Base):
    '''Класс объявлений'''
    __tablename__ = "advertisement"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(600))
    create_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    # Связь с пользователем
    owner = relationship("User", back_populates="advertisements")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description":self.description,
            "create_time": self.create_date.isoformat(),
            "owner": self.owner.username
        }

Base.metadata.create_all(bind=engine)