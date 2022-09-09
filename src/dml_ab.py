import sqlalchemy
from sqlalchemy import and_
import src.models as mod
from src.db import session


class Decorator:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except sqlalchemy.exc.NoResultFound:
            print('Not found this command')


@Decorator
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


@Decorator
def remove_all():
    session.query(mod.AddressBook).filter(mod.AddressBook.id != 0).delete()
    print('Successfully remove all users')
    session.commit()


@Decorator
def remove_user(name):
    session.query(mod.AddressBook).filter(mod.AddressBook.name == name).delete()
    print(f'Successful remove user {name}')
    session.commit()


@Decorator
def add_email(name, email):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.email = email
    print(f"Successful add email to {name}")


@Decorator
def show_all():
    users = session.query(mod.AddressBook).all()
    for u in users:
        print(f'Id: {u.id} for user: {u.name}, phone: {u.phone}, birthday: {u.birthday}, email: {u.phone}, address: {u.address}')
    session.commit()


@Decorator
def change_contact(name, old, new):
    old_data = session.query(mod.AddressBook).filter(and_(mod.AddressBook.phone == old, mod.AddressBook.name == name)).one()
    old_data.phone = new
    print(f'Successful change phone number')
    session.commit()


@Decorator
def show_phone(name):
    user = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    print(f'{user.phone}')
    session.commit()


@Decorator
def del_phone(name):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.phone = ''
    print(f"Successful remove phone in user: {name}")
    session.commit()


@Decorator
def add_birthday(name, birthday):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.birthday = birthday
    print(f"Successful add email to {name}")
    session.commit()


@Decorator
def find_user(name):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    session.commit()
    return sel.birthday


@Decorator
def del_email(name):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.email = ''
    session.commit()
    print(f'Successful delete email from user: {name}')


@Decorator
def add_address(name, address):
    sel = session.query(mod.AddressBook).filter(mod.AddressBook.name == name).one()
    sel.address = address
    print(f'Add/modify address {address} to user: {name}')


@Decorator
def find_something(som):
    sel = session.query(mod.AddressBook).all()
    som_st = ' '.join(som)
    for s in sel:
        birthday = s.birthday.strftime("%Y-%m-%d")
        if som_st in s.name or som_st in s.phone or som_st in birthday or som_st in s.email or som_st in s.address:
            print(f'User {s.name}, phone: {s.phone}, birthday: {s.birthday}, email: {s.email}, address: {s.address}')


if __name__ == "__main__":
    pass