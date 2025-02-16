# pylint: disable=invalid-name
"""
This module defines the base class for SQLAlchemy ORM models.

Classes:
    - Base: The declarative base class for all ORM models.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
