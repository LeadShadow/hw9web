from sqlalchemy.exc import ProgrammingError, NoResultFound
from sqlalchemy.orm import joinedload

from src.dml_ab import Decorator
from src.db import session
from src.models import Note, Archive, Tag, TagsNotes


notes = session.query(Note).all()
tags = session.query(Tag).all()

for n in notes:
    for t in tags:
        rel = TagsNotes(notes_id=n.id, tags_id=t.id)
        session.add(rel)
        break
session.commit()


def add_note(text):
    note = Note(description=text)
    session.add(note)
    print('Successful add note')
    session.commit()


def change_note(id_, text):
    sel = session.query(Note).filter(Note.id == id_).one()
    sel.description = text
    print(f'Successful change text in note {id_}')
    session.commit()


def del_note(id_):
    session.query(Note).filter(Note.id == id_).delete()
    print(f'Successful delete note {id_}')
    session.commit()


def add_date(id_, date):
    sel = session.query(Note).filter(Note.id == id_).one()
    sel.date = date
    print(f'Successful add date to note {id_}')
    session.commit()


def show_all():
    sel = session.query(Note).all()
    for s in sel:
        print(f'Note id: {s.id}, date: {s.created}, done: {bool(s.done)}\n'
              f'Text: {s.description}\n'
              f'---------------------------------------------------------\n')
    session.commit()


def done_note(id_):
    try:
        sel_arc = session.query(Archive).filter(Archive.id == id_).one()
        print(f'Note with id: {id_} in archives')
    except NoResultFound:
        print('Note not in archives')
    try:
        sel_note = session.query(Note).options(joinedload('tags')).filter(Note.id == id_).one()
        arc = Archive(id=sel_note.id,
                      description=sel_note.description,
                      tag=sel_note.tags)
        print(f'Note with id: {id_} added to archives')
        session.query(Note).filter(Note.id == id_).delete()
        session.add(arc)
        session.commit()
    except NoResultFound:
        print('Note not in notes')


def show_archived():
    sel = session.query(Archive).all()
    for s in sel:
        print(f'Note id: {s.id}, date: {s.transferred}, tag: {s.tag}\n'
              f'Text: {s.description}\n'
              f'---------------------------------------------------------\n')
    session.commit()


def find_note(text):
    sel = session.query(Note).all()
    som_st = ' '.join(text)
    for s in sel:
        created = s.created.strftime("%Y-%m-%d %H:%M:%S")
        if som_st in s.description or som_st in created:
            print(f'Note: {s.id}, description: {s.description}, created: {s.created}')


def return_note(id_):
    sel_arc = session.query(Archive).filter(Archive.id == id_).one()
    print(type(sel_arc.tag))
    note = Note(id=sel_arc.id,
                description=sel_arc.description)
    session.add(note)
    session.query(Archive).filter(Archive.id == id_).delete()
    session.commit()
    print(f'Note with id {id_} return successful')


def add_tag(id_, tags):
    list_tags = []
    for i in tags:
        sel_tag = Tag(id=id_, tag=i)
        list_tags.append(sel_tag)
        session.add(sel_tag)
    print(f'Tag/s added successfully to note with id {id_}')
    session.commit()
    note_ = session.query(Note).options(joinedload('tags')).filter(Note.id == id_).one()
    vars_n = vars(note_)
    vars_n['tags'] = list_tags


# def find_tag(tag):
#     str_tag = ' '.join(tag)
#     notes_ = session.query(Note).options(joinedload('tags')).all()
#     for n in notes_:
#         vars_n = vars(n)
#         print(vars_n)
#         for i in vars_n['tags']:
#             print(i.tag)
#         if str_tag in vars_n['tags']:
#             print(f'Note id: {n.id}, date: {n.created}, done: {bool(n.done)}\n'
#                   f'Text: {n.description}\n'
#                   f'Tags: {vars_n["tags"]}\n'
#                   f'---------------------------------------------------------\n')


if __name__ == "__main__":
    id_ = input("input id >>> ")
    tags = input("input tags >>> ")
    add_tag(int(id_), tags)
