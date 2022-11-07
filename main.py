import sys
from json import *

running = True

def loop():
    """boucle principale du programme"""

    while running:
        command = inputInt("Entrez votre commande ici: ")
        if command == 0:
            exit()
        elif command == 1:
            add()
        elif command == 2:
            get()


def exit():
    """fonction pour sortir du programme"""
    sys.exit(0)

def add():
    """fonction pour ajouter un nouveau contact"""
    loop = True
    while loop:
        name = inputStr("Nom (0 pour terminer)")
        if name == 0:
            loop = False
            continue

        num = inputPhoneNumber("Numéro de téléphone: ")
        #if num is None retry

    pass

def get():
    """fonction pour récupérer  un contact"""
    pass

#                                   #-----****-----#                                   #

def inputInt(*title):
    """fonction qui permet d'input un integer"""
    try:
        return int(inputValue(title))
    except ValueError:
        pass

def inputStr(*title):
    """fonction qui permet d'input un string"""
    try:
        return str(inputValue(title))
    except ValueError:
        pass

def inputPhoneNumber(*title):
    """fonction qui permet d'input un phone number"""
    inp = inputInt(title)
    if inp is None:
        return
    inp = str(inp)

    if len(inp) != 10:
        return

    return inp


def inputValue(title):
    """fonction qui permet d'input une valeur"""

    while type(title) == tuple:
        if len(title) != 0:
            title = title[0]
        else:
            title = ""
            break
    return input(title)

