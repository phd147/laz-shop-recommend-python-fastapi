from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from sqlalchemy.orm import relationship
from ..shared.database import Base


class Reaction(Base):
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    star = Column(Integer)
    item_id = Column(Integer)
    user_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


