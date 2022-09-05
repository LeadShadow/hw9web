from sqlalchemy import and_
from sqlalchemy.orm import joinedload

import src.models as mod
from src.db import session


def insert_adressbook(name, phone, birthday, emails, address):
    emails_str = ''
    for i in emails:
        emails_str += i.value + ' '
    ab_ = mod.AddressBook(
        name=name.value,
        phone=phone.value,
        birthday=birthday.value,
        email=emails_str,
        address=address.value
    )
    session.add(ab_)
    print(f'add user {name} into database')
    session.commit()


def remove_all():
    name = session.query(mod.AddressBook).filter(mod.AddressBook.id != 0).delete()
    print('Successfully remove all users')
    session.commit()


def remove_user(name):
    session.query(mod.AddressBook).filter(mod.AddressBook.name == name).delete()
    print(f'Successful remove user {name}')
    session.commit()


def add_email(name, email):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.email = f"{sel.email}, {email}"
    print(f"Successful add email to {name}")


def show_all():
    users = session.query(mod.AddressBook).all()
    for u in users:
        print(f'{u.id} for user {u.name} his phone, birthday, email, address: {u.phone}, {u.birthday}, {u.email}, {u.address}')
    session.commit()


def change_contact(name, old, new):
    old_data = session.query(mod.AddressBook).filter(and_(mod.AddressBook.phone == old, mod.AddressBook.name == name)).one()
    old_data.phone = new
    print(f'Successful change phone number')
    session.commit()


def show_phone(name):
    user = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    print(f'{user.phone}')
    session.commit()


def del_phone(name):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.phone = ''
    print(f"Successful remove phone in user: {name}")
    session.commit()


def add_birthday(name, birthday):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.birthday = birthday
    print(f"Successful add email to {name}")
    session.commit()


def find_user(name):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    session.commit()
    return sel.birthday


def del_email(name):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.email = ''
    session.commit()
    print(f'Successful delete email from user: {name}')


def add_address(name, address):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.address = address
    print(f'Add/modify address {address} to user: {name}')

if __name__ == "__main__":
    pass