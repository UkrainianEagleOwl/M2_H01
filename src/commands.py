

from output_module import output_for_user
from input_module import get_command_input
from memory import Record, AddressBook, Phone
from notes_core import *
from sorter import sort_files_in_this_path


def input_error(func):
    def wrapper(*arg, a_book=AddressBook, n_book=Notebook):
        try:
            result = func(*arg, a_book=a_book, n_book=n_book)
            return result
        except KeyError:
            output_for_user.show_message(
                Fore.RED + "The contact is missing. Please try again" + Style.RESET_ALL
            )
        except IndexError:
            output_for_user.show_message(
                Fore.RED + "The contact is missing. Please try again" + Style.RESET_ALL
            )
        except ValueError:
            output_for_user.show_message(
                Fore.RED + "ValueError. Please try again." + Style.RESET_ALL
            )

    return wrapper


def greetings(*arg, a_book=AddressBook, n_book=Notebook):
    return "Hello. How i can help you?"


@input_error
def add_new_contact(*arg, a_book=AddressBook, n_book=Notebook):
    rec = Record(
        name=arg[0].capitalize(),
        phone=arg[1],
        birthday=arg[2],
        email=arg[3],
        address=arg[4],
    )
    a_book.add_record(rec)
    while True:
        input_bool = get_command_input(
            "Do you want to add more phone numbers? Write Yes or No: ", need_comp=False
        )
        if input_bool.lower() == "yes":
            new_phone = get_command_input(
                "Enter additional phone: ", Phone, need_comp=False
            )
            rec.add_phone(new_phone)
        elif input_bool.lower() == "no":
            break

    output_for_user.show_message("Contact added.")


@input_error
def change_exist_contact(*arg, a_book=AddressBook, n_book=Notebook):
    contact = a_book.get(arg[0])
    if contact:
        contact.change_record_info(arg[1], arg[2])
        output_for_user.show_message(f"Contact's phone was changed.")
    else:
        output_for_user.show_message("Can't find such contact. Try again.")


@input_error
def show_contact(
    *arg, a_book=AddressBook, n_book=Notebook
):  # first always address book second name
    if arg[0] in a_book.data:
        output_for_user.show_contact(a_book.data[arg[0]])
    else:
        output_for_user.show_message(f"Contact {arg[0]} does not exist. ")


def show_all(*arg, a_book=AddressBook, n_book=Notebook):
    output_for_user.show_addressbook(a_book)


@input_error
def find_user(*arg, a_book=AddressBook, n_book=Notebook):
    results = a_book.find_users(arg[0])
    (
        output_for_user.show_contact(result) for result in results
    ) if results else output_for_user.show_message("No matches found among contacts.")


def help_commands(*arg, a_book=AddressBook, n_book=Notebook):
    output_for_user.show_help(commands)


@input_error
def remove_contact(*arg, a_book=AddressBook, n_book=Notebook):
    a_book.remove_record(arg[0])
    output_for_user.show_message("Contact was removed.")


def sort_files(
    *arg, a_book=AddressBook, n_book=Notebook
):  # first ALWAYS address book. next every you need, just ignore the first
    sort_files_in_this_path(arg[0])


@input_error
def add_note(*arg, a_book=AddressBook, n_book=Notebook):
    tags = get_command_input(
        "Enter note tags (comma-separated):", need_comp=False
    ).split(",")
    tags = [Tag(tag.strip()) for tag in tags]
    note = Note(arg[0], tags, arg[1])
    n_book.add_note(note)
    output_for_user.show_message("Note added.")


@input_error
def remove_note(*arg, a_book=AddressBook, n_book=Notebook):
    title = arg[0]
    n_book.remove_note(title)
    output_for_user.show_message("Note removed.")


@input_error
def find_notes(*args, a_book=AddressBook, n_book=Notebook):
    text = args[0]
    matching_notes_strings = n_book.search_notes_by_text(text)
    if matching_notes_strings:
        output_for_user.show_notes(matching_notes_strings)
    else:
        output_for_user.show_message("No notes found for the given text.")


@input_error
def edit_note_info(*arg, a_book=AddressBook, n_book=Notebook):
    note = n_book.search_notes_by_title(arg[0])
    if note:
        note.change_note_info(arg[1], arg[2])
        if arg[1] == "tag":
            while True:
                input_bool = get_command_input(
                    "Do you want to add more tags? Write Yes or No: ", need_comp=False
                )
                if input_bool.lower() == "yes":
                    new_tag = get_command_input("Enter tag:", Tag, need_comp=False)
                    note.add_tag(new_tag)
                elif input_bool.lower() == "no":
                    break
        output_for_user.show_message("Note information updated.")
    else:
        output_for_user.show_message("Note not found.")


@input_error
def search_notes_by_tag(*arg, a_book=AddressBook, n_book=Notebook):
    tag_name = arg[0]
    matching_notes_strings = n_book.search_notes_by_tag(tag_name)
    if matching_notes_strings:
        output_for_user.show_notes(matching_notes_strings)
    else:
        output_for_user.show_message("No notes found for the given tag.")


@input_error
def sort_notes_by_tag(*arg, a_book=AddressBook, n_book=Notebook):
    n_book.sort_notes_by_tag()
    output_for_user.show_message("Notes sorted by tags.")


def show_all_notes(*arg, a_book=AddressBook, n_book=Notebook):
    output_for_user.show_notebook(n_book)


def start_game(*arg, a_book=AddressBook, n_book=Notebook):
    output_for_user.show_message("Starting the game...")


def ending(*arg, a_book=AddressBook, n_book=Notebook):
    output_for_user.show_message("Goodbye!")


# Define available commands
commands = [
    {
        "name": "greet",
        "input view": ["hello", "hi", "start"],
        "arguments": [],
        "func": greetings,
    },
    {
        "name": "game",
        "input view": ["game", "play", "fun"],
        "arguments": [],
        "func": start_game,
    },
    {
        "name": "add new contact",
        "input view": ["add contact", "new contact", "create contact"],
        "arguments": ["name", "phone", "birthday", "email", "address"],
        "func": add_new_contact,
    },
    {
        "name": "change exist contact",
        "input view": ["change contact", "change phone", "change contact details"],
        "arguments": ["name", "changed field", "new value"],
        "func": change_exist_contact,
    },
    {
        "name": "remove contact",
        "input view": ["remove contact", "delete contact", "take out contact"],
        "arguments": ["name"],
        "func": remove_contact,
    },
    {
        "name": "show contact",
        "input view": ["get contact", "show contact", "show person"],
        "arguments": ["name"],
        "func": show_contact,
    },
    {
        "name": "show all",
        "input view": ["show contacts", "show address book", "show all book"],
        "arguments": [],
        "func": show_all,
    },
    {
        "name": "find user",
        "input view": ["search user", "find contact", "find user"],
        "arguments": ["text_for_search"],
        "func": find_user,
    },
    {
        "name": "help",
        "input view": ["help", "commands", "need help"],
        "arguments": [],
        "func": help_commands,
    },
    {
        "name": "sort",
        "input view": ["sort", "sort files", "need sort"],
        "arguments": ["path to the folder"],
        "func": sort_files,
    },
    {
        "name": "add_note",
        "input view": ["add note", "new note", "create note"],
        "arguments": ["title", "description"],
        "func": add_note,
    },
    {
        "name": "remove_note",
        "input view": ["remove note", "delete note", "get note out"],
        "arguments": ["title"],
        "func": remove_note,
    },
    {
        "name": "find_notes",
        "input view": ["find notes", "search notes", "give me note"],
        "arguments": ["text"],
        "func": find_notes,
    },
    {
        "name": "edit note info",
        "input view": ["edit note", "change note", "remake note"],
        "arguments": ["title", "changed field", "new info"],
        "func": edit_note_info,
    },
    {
        "name": "search notes by tag",
        "input view": ["search by tag", "find by tag", "give me note by tag"],
        "arguments": ["tag name"],
        "func": search_notes_by_tag,
    },
    {
        "name": "sort notes by tag",
        "input view": ["sort by tag", "tag sorting", "notebook sort by tag"],
        "arguments": [],
        "func": sort_notes_by_tag,
    },
    {
        "name": "show all notes",
        "input view": ["show all notes", "show notebook", "show notes"],
        "arguments": [],
        "func": show_all_notes,
    },
    {
        "name": "ending",
        "input view": ["goodbye", "close", "end"],
        "arguments": [],
        "func": ending,
    },
]
