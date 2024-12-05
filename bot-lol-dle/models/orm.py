from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class AssetModel(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
