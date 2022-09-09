from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from datetime import datetime
import colorama
import re

from console_bot.command_parser import command_parser, RainbowLexer
import src.dml_ab as dml


N = 3  # кількість записів для представлення телефонної книги


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other) -> bool:
        return self.value == other.value


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        def is_code_valid(phone_code: str) -> bool:
            if phone_code[:2] in ('03', '04', '05', '06', '09') and phone_code[2] != '0' and phone_code != '039':
                return True
            return False

        result = None
        phone = value.removeprefix('+').replace('(', '').replace(')', '').replace('-', '')
        if phone.isdigit():
            if phone.startswith('0') and len(phone) == 10 and is_code_valid(phone[:3]):
                result = '+38' + phone
            if phone.startswith('380') and len(phone) == 12 and is_code_valid(phone[2:5]):
                result = '+' + phone
            if 10 <= len(phone) <= 14 and not phone.startswith('0') and not phone.startswith('380'):
                result = '+' + phone
        if result is None:
            raise ValueError(f'Неправильний тип значення {value}')
        self.__value = result


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return '-'
        else:
            return f'{self.value:%d %b %Y}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                try:
                    self.__value = datetime.strptime(value, '%d.%m.%Y').date()
                except ValueError:
                    raise DateIsNotValid


class Address(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        self.__value = value

    def __str__(self):
        if self.value is None:
            return '-'
        else:
            return f'{self.value}'


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            result = None
            get_emails = re.findall(r'\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
            if get_emails:
                for i in get_emails:
                    result = i
            if result is None:
                raise AttributeError(f"Неправильний тип значення {value}")
            self.__value = result


class Record:
    def __init__(self, name: Name, phones=[], birthday=None, emails=[], address=None) -> None:
        self.name = name
        self.phone_list = phones
        self.birthday = birthday
        self.address = address
        self.email_list = emails

    def __str__(self) -> str:
        if self.email_list:
            emails = ',\n            '.join([email.value for email in self.email_list])
        else:
            emails = '-'
        return f' User \033[35m{self.name.value:20}\033[0m Birthday: {self.birthday}\n' \
               f'     Phones: {", ".join([phone.value for phone in self.phone_list])}\n' \
               f'     Email: {emails}\n' \
               f'     Address: {self.address}'


def days_to_birthday(birthday: str):
    if birthday is None:
        return None
    this_day = datetime.today()
    birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
    birthday_day = datetime(this_day.year, birthday_date.month, birthday_date.day)
    if birthday_day < this_day:
        birthday_day = datetime(this_day.year + 1, birthday_date.month, birthday_date.day)
    return (birthday_day - this_day).days


class PhoneUserAlreadyExists(Exception):
    """You cannot add an existing phone number to a user"""


class EmailUserAlreadyExists(Exception):
    """You cannot add an existing email to a user"""


class DateIsNotValid(Exception):
    """You cannot add an invalid date"""


class EmailIsNotValid(Exception):
    """Email is not valid, try again"""


class FindNotFound(Exception):
    """Find is not valid, try again"""


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, contacts, *args):
        try:
            return self.func(contacts, *args)
        except IndexError:
            return 'Error! Give me name and phone or birthday please!'
        except KeyError:
            return 'Error! User not found!'
        except ValueError:
            return 'Error! Phone number is incorrect!'
        except PhoneUserAlreadyExists:
            return 'Error! You cannot add an existing phone number to a user'
        except EmailUserAlreadyExists:
            return 'Error! You cannot add an existing email to a user'
        except DateIsNotValid:
            return 'Error! Date is not valid'
        except AttributeError:
            return 'Error! Email is not valid'
        except FindNotFound:
            return 'Error! Try command find or search "words" that find contact'


def salute(*args):
    return 'Hello! How can I help you?'


@InputError
def add_contact(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = None
    emails = []
    address = None
    if len(args) > 2:
        birthday = Birthday(args[2])
    if len(args) > 3:
        emails = [Email(args[3])]
    if len(args) > 4:
        address = Address(" ".join(args[4:]))
    if len(args) <= 2:
        birthday = Birthday(None)
    if len(args) <= 3:
        emails = []
    if len(args) <= 4:
        address = Address(None)
    dml.insert_adressbook(name, phone, birthday, emails, address)


@InputError
def change_contact(*args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    dml.change_contact(name, old_phone, new_phone)


@InputError
def show_phone(*args):
    name = args[0]
    dml.show_phone(name)


@InputError
def del_phone(*args):
    name = args[0]
    dml.del_phone(name)


def show_all(*args):
    dml.show_all()


@InputError
def add_birthday(*args):
    name, birthday = args[0], args[1]
    dml.add_birthday(name, birthday)


@InputError
def days_to_user_birthday(*args):
    name = args[0]
    birthday = dml.find_user(name)
    if birthday is None:
        print('User has no birthday')
    print(f'{days_to_birthday(birthday)} days to birthday user {name}')


def goodbye(*args):
    print('You have finished working with addressbook')


@InputError
def search(*args):
    if len(args) >= 1:
        dml.find_something(args)
    else:
        raise FindNotFound


@InputError
def del_user(*args):
    name = args[0]
    yes_no = input(f'Are you sure you want to delete the user {name}? (Y/n) ')
    if yes_no == 'Y':
        dml.remove_user(name)
    else:
        print('User not deleted')


def clear_all(*args):
    yes_no = input('Are you sure you want to delete all users? (Y/n) ')
    if yes_no == 'Y':
        dml.remove_all()
    else:
        print('Removal canceled')


@InputError
def add_email(*args):
    name, email = args[0], Email(args[1])
    dml.add_email(name, email.value)


@InputError
def del_email(*args):
    name, email = args[0], args[1]
    dml.del_email(name)


@InputError
def add_address(*args):
    name, address = args[0], " ".join(args[1:])
    dml.add_address(name, address)


def help_me(*args):
    print("""\nCommand format:
    help or ? - this help;
    hello - greeting;
    add <name> <phone> [<birthday>] - add user to directory;
    change <name> <old_phone> <new_phone> - change the user's phone number;
    del phone <name> <phone> - delete the user's phone number;
    delete <name> - delete the user;
    clear - delete all users;
    birthday <name> <birthday> - add/modify the user's birthday;
    email <name> <email> - add the user's email;
    del email <name> <email> - delete the user's email;
    address <name> <address> - add/modify the user's address;
    show <name> - show the user's data;
    show all - show data of all users;
    find or search <sub> - show data of all users with sub in name, phones or birthday;
    days to birthday <name> - show how many days to the user's birthday;
    show birthday days <N> - show the user's birthday in the next N days;
    good bye or close or exit or . - exit the program""")


COMMANDS_A = {salute: ['hello'], add_contact: ['add '], change_contact: ['change '], help_me: ['?', 'help'],
              show_all: {'show all'}, goodbye: ['good bye', 'close', 'exit', '.'], del_phone: ['del phone '],
              add_birthday: ['birthday'], days_to_user_birthday: ['days to birthday '],
              show_phone: ['show '], search: ['find ', 'search '],
              del_user: ['delete '], clear_all: ['clear'], add_email: ['email '], add_address: ['address'],
              del_email: ['del email']}


def start_ab():
    print('\n\033[033mWelcome to the address book!\033[0m')
    print(f"\033[032mType command or '?' for help \033[0m\n")
    while True:
        with open("history.txt", "wb"):
            pass
        user_command = prompt('Enter command >>> ',
                              history=FileHistory('history.txt'),
                              auto_suggest=AutoSuggestFromHistory(),
                              completer=Completer,
                              lexer=RainbowLexer()
                              )
        command, data = command_parser(user_command, COMMANDS_A)
        command(*data), '\n'
        if command is goodbye:
            break


Completer = NestedCompleter.from_nested_dict({'help': None, 'hello': None, 'good bye': None, 'exit': None,
                                              'close': None, '?': None, '.': None, 'birthday': None,
                                              'days to birthday': None, 'add': None,
                                              'show all': None, 'change': None, 'del': {'phone': None, 'email': None}, 'delete': None,
                                              'clear': None, 'email': None, 'find': None, 'search': None,
                                              'address': None})

if __name__ == "__main__":
    start_ab()
