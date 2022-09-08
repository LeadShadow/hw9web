from random import randint

from sqlalchemy.orm import Session

from src.models import Note, Tag
from src.db import engine

with Session(engine) as session:
    tag1 = Tag(name=f'Tag{str(randint(1, 1000))}')
    tag2 = Tag(name=f'Tag{str(randint(1, 1000))}')

    note1 = Note(name=f'Note{str(randint(1, 1000))}', tags=[tag1, tag2])

    session.add_all([tag1, tag2, note1])

    session.commit()

    tag = session.get(Tag, 1)

    session.add(tag)

    note2 = Note(name=f'2Note{str(randint(1, 1000))}', tags=[tag])

    session.add(note2)

    session.commit()

    note = session.get(Note, 1)

    print(note.tags)
