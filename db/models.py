"""Collection of DB entities for the Feature Flags microservice."""

from sqlalchemy import Boolean, String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
matadata = Base.metadata


class FeatureFlag(Base):
    """Feature Flag model representation."""

    __tablename__ = 'feature_flags'

    id = Column(Integer(), autoincrement=True, primary_key=True)

    name = Column(String(100), nullable=False)
    is_active = Column(Boolean(), nullable=False, default=False)
