from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    tags = relationship("Tag", secondary=association_table,
                        back_populates="notes")


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)
    done = Column(Boolean, default=False)
    note_id = Column(Integer, ForeignKey(Note.id, ondelete='CASCADE'))


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)
    notes = relationship(
        "Note", secondary=association_table, back_populates="tags")

    def __repr__(self) -> str:
        return f'{self.name}'


# class TagsNotes(Base):
#     __tablename__ = 'tags_to_notes'
#     id = Column(Integer, primary_key=True)
#     notes_id = Column('notes_id', ForeignKey('notes.id', ondelete='CASCADE'))
#     tags_id = Column('tags_id', ForeignKey('tags.id', ondelete='CASCADE'))


if __name__ == "__main__":
    engine = create_engine("sqlite:///db.db", echo=True, future=True)
    Base.metadata.create_all(engine)
