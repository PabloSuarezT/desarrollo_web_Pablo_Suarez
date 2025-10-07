from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "tarea2"
DB_USERNAME = "root"
DB_PASSWORD = "P7677Joder"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_CHARSET = "utf8"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

Base = declarative_base()

#-- Models --

class Comuna(Base):
    __tablename__ = "comuna"

    id = Column( Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'),nullable=False)

    region = relationship('Region', backref='comunas')

class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key= True, autoincrement=True)
    nombre = Column(String(200), nullable=False)


