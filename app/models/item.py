from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from sqlalchemy.orm import relationship
from ..shared.database import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer,)
    name = Column(String)
    price = Column(Integer)
    amount = Column(Integer)
    image_url = Column(String)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    description = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    length = Column(Integer)
    width = Column(Integer)
    is_active = Column(Boolean)
