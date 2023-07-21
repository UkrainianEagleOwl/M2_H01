

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import difflib
from src.output_module import output_for_user
from src.constants import *
from src.memory import SetterValueIncorrect

# Ініціалізація автодоповнювача зі списком команд
completer = WordCompleter(input_variants)

def get_command_input_agree(Input_message=''):
    Input_value = None
    while True:
        Input_value = prompt(Input_message)
        if (Input_value.lower() == 'yes') or (Input_value.lower() == 'no'):
            return Input_value
        else:
            output_for_user.show_message("You can write only 'yes' or 'no'!")

def get_command_input(Input_message='',check_class = None,need_comp = True, check_add_command = None, arg_number = None):
    Input_value = None
    while True:
        if need_comp:
            Input_value = prompt(Input_message, completer=completer)
        else:
            Input_value = prompt(Input_message)
        if Input_value == 'pass':
            Input_value = None
        if check_class:
            try:
                check_obj = check_class(Input_value)
            except SetterValueIncorrect as e:
                output_for_user.show_message(e.message)
            else:
                break
        elif check_add_command and (arg_number == 1):
            if check_add_command["name"] == "change exist contact":
                if Input_value in CHECK_SECOND_ARG_CHANGE_CONTACT:
                    break
                else:
                    output_for_user.show_message(f'You can write only {CHECK_SECOND_ARG_CHANGE_CONTACT}')
            elif check_add_command["name"] == 'edit note info':
                if Input_value in CHECK_SECOND_ARG_CHANGE_NOTE:
                    break
                else:
                    output_for_user.show_message(f'You can write only {CHECK_SECOND_ARG_CHANGE_NOTE}')
            elif Input_value:
                break
        elif Input_value:
            break
    return Input_value

#Функція find_closest_command(user_input) знаходить найближчу команду до введеної користувачем, за допомогою алгоритму Левенштейну.
def find_closest_command(user_input,list_commands):
    cmd = None
    closest_command = difflib.get_close_matches(user_input, input_variants, n=1)
    if closest_command:
        closest_command = closest_command[0]
        for command_dict in list_commands:
            if closest_command in command_dict["input view"]:
                cmd = command_dict
        if cmd:
            return cmd
        else:
            return None
    else:
        return None