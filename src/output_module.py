from abc import abstractmethod, ABCMeta
from memory import *
from constants import STR_EPIC_COMMANDS
from notes_core import *


class OutputForUser(metaclass=ABCMeta):
    @abstractmethod
    def show_contact(self, rrecord=Record):
        pass

    @abstractmethod
    def show_addressbook(self, ra_book=AddressBook):
        pass

    @abstractmethod
    def show_help(self):
        pass

    @abstractmethod
    def show_message(self, rstr):
        pass

    @abstractmethod
    def show_note(self, rnote=Note):
        pass

    @abstractmethod
    def show_notebook(self, rn_book=Notebook):
        pass


class ConsoleOutputForUser(OutputForUser):
    def show_contact(self, record=Record):
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Birthday", "Email", "Address"]
        phone_numbers = ", ".join(str(phone) for phone in record.user_phones)
        table.add_row(
            [
                record.user_name,
                phone_numbers,
                record.user_birthday,
                record.user_email,
                record.user_address,
            ]
        )
        print(str(table))

    def show_help(self, commands_dict):
        l_cmd = []
        l_cmd.append(STR_EPIC_COMMANDS)
        for cmd in commands_dict:
            s = "Command: " + Fore.YELLOW + f"{cmd.get('name')}" + Style.RESET_ALL
            s2 = (
                "Write: "
                + Fore.GREEN
                + f"{cmd['input view'][0]}"
                + Style.RESET_ALL
                + ","
                + Fore.GREEN
                + f" {cmd['input view'][1]}"
                + Style.RESET_ALL
                + " or "
                + Fore.GREEN
                + f"{cmd['input view'][2]}"
                + Style.RESET_ALL
            )
            s = "|{:<40}|{:<95}|".format(s, s2)
            if len(cmd["arguments"]) > 0:
                s3 = "Arguments: " + Fore.BLUE + f"{cmd['arguments']}" + Style.RESET_ALL
                s3 = "{:<50}".format(s3)
                s += s3
            l_cmd.append(s)
        for i in l_cmd:
            print(i)

    def show_message(self, str):
        print(str)

    def show_addressbook(self, a_book=AddressBook):
        table = PrettyTable()
        table.field_names = ["№", "Name", "Phone", "Email", "Date of Birth", "Address"]
        # сортування за "user_name"
        sorted_data = sorted(a_book.values(), key=lambda x: x.user_name.value)
        counter = 1
        for user_data in sorted_data:
            phones = user_data.user_phones
            formatted_numbers = []
            for number in phones:
                formatted_number = str(number)
                formatted_numbers.append(formatted_number)
            formatted_phone = "\n".join(formatted_numbers)
            table.add_row(
                [
                    counter,
                    user_data.user_name,
                    formatted_phone,
                    user_data.user_email,
                    user_data.user_birthday,
                    user_data.user_address,
                ]
            )
            counter += 1
        print(table)

    def show_note(self, note=Note):
        tags_str = ""
        if note.tags:
            tags_str = ", ".join(tag.name for tag in note.tags)
        print(
            "Title: {}\nTags: {}\nDescription: {}".format(
                note.title, tags_str, note.description
            )
        )

    def show_notebook(self, n_book=Notebook):
        if not n_book.notes:
            print("Notebook is empty.")
        else:
            table = n_book.put_notes_in_stringlist(n_book.notes)
            for i in table:
                print(i)

    def show_notes(self, string_list):
        for i in string_list:
            print(i)


output_for_user = (
    ConsoleOutputForUser()
)  # if in console create object console if not create another object
