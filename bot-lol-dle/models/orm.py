from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()

class AssetModel(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<AssetModel(id={self.id}, nom={self.nom}, path={self.path})>"
