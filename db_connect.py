# import os
from sqlalchemy import Sequence, create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from geoalchemy2 import Geometry
# from dotenv import load_dotenv

# load_dotenv()


# db_params = sqlalchemy.URL.create(
#     drivername='postgresql+psycopg2',
#     username=os.getenv('POSTGRES_USER'),
#     password=os.getenv('POSTGRES_PASSWORD'),
#     host=os.getenv('POSTGRES_HOST'),
#     database=os.getenv('POSTGRES_DB'),
#     port=os.getenv('POSTGRES_PORT')
# )
db_params = sqlalchemy.URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='123',
    host='localhost',
    database='postgres',
    port=5432
)

engine = create_engine(db_params)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Military_training_ground(Base):
    __tablename__ = "Military_training_grounds"
    
    id = Column(Integer(), Sequence("user_id_seq"),primary_key=True)
    name = Column(String(100),nullable=True)
    location = Column('geom', Geometry(geometry_type='POLYGON', srid=4326), nullable=True)

    def __init__(self, name, area):
        self.name = name
        self.location = f"POLYGON({area})"

class Soldier(Base):
    __tablename__ = "Soldiers"
    
    id = Column(Integer(), Sequence("user_id_seq"),primary_key=True)
    name = Column(String(100),nullable=True)
    role = Column(String(100),nullable=True)
    polygon = Column(String(100),nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)
    
    def __init__(self, name, polygon, role, location):
        self.name = name
        self.polygon = polygon
        self.role = role
        self.location = f'POINT({location[1]} {location[0]})'
        
Base.metadata.create_all(engine)