from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.db import Base


association_table = Table(
    "tag_to_notes",
    Base.metadata,
    Column("notes_id", ForeignKey("notes.id")),
    Column("tags_id", ForeignKey("tags.id")),
)


class AddressBook(Base):
    __tablename__ = 'contacts'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(75), nullable=False)
    phone = Column('phone', String(50), nullable=True)
    birthday = Column('birthday', DateTime, nullable=True)
    email = Column('email', String(100), nullable=True)
    address = Column('address', String(100), nullable=True)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)
    done = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now())
    tags = relationship("Tag", secondary=association_table, back_populates="notes")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(60), nullable=False, unique=True)
    notes = relationship("Note", secondary=association_table, back_populates="tags")


class Archive(Base):
    __tablename__ = "archives"
    id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)
    transferred = Column(DateTime, default=datetime.now())
    tag = Column(String(60), nullable=False)


# class TagsNotes(Base):
#     __tablename__ = 'tags_to_notes'
#     id = Column(Integer, primary_key=True)
#     notes_id = Column('notes_id', ForeignKey('notes.id', ondelete='CASCADE'))
#     tags_id = Column('tags_id', ForeignKey('tags.id', ondelete='CASCADE'))
