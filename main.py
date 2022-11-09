import json
import sys

running = True

FILE = "data.json"

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
        elif command == 3:
            delete()


def exit():
    """fonction pour sortir du programme"""
    sys.exit(0)

def add():
    """fonction pour ajouter un nouveau contact"""
    loop = True
    while loop:
        name = inputStr("Nom (0 pour terminer): ")
        if name == '0':
            break

        if exist(name):
            print("Erreur: ce nom exist deja !")
            continue

        num = inputPhoneNumber("Numero de telephone: ")
        if num is None:
            print("Erreur: le numero de telephone n'est pas valide !")
            continue

        addContact(name, num)

    pass

def get():
    """fonction pour recuperer  un contact"""
    loop = True
    while loop:
        name = inputStr("Nom (0 pour terminer): ")
        if name == '0':
            break

        result = getContact(name)

        if result == None:
            print("Erreur: le nom est introuvable")
            continue

        print("Le numero de telephone de " + name + " est: " + result)
        return

    pass

def delete():
    loop = True
    while loop:
        name = inputStr("Nom (0 pour terminer): ")
        if name == '0':
            break

        if not exist(name):
            print("Erreur: " + name + "n'existe pas !")
            continue

        if not consent("Etes-vous sur de vouloir supprimer " + name + " ?", True):
            print("[End]")
            continue

        delContact(name)
        print(name + " a bien ete supprime")



def exist(name):
   return index(name) is not None

def index(name):
    content = getFile()
    for i in content:
        if i['name'] == name:
            return i

def addContact(name, number):
    content = getFile()

    content.append({"name": name, "number": number})
    writeFile(content)

def getContact(name):
    i = index(name)
    if i is not None:
        return i['number']

def delContact(name):
    i = index(name)
    if i is None:
        return

    content = getFile()

    content.remove(i)
    writeFile(content)

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
    inp = '0' + inp

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

def getFile():
    """recupere le contenu du fichier"""
    if empty():
        clear()

    with open(FILE, "r") as f:
        return json.load(f)

def empty():
    with open(FILE, "r") as f:
        return len(f.read()) == 0


def clear():
    with open(FILE, "w") as f:
        json.dump([], f)

def writeFile(data):
    """ecrit le contenu du fichier"""
    with open(FILE, "w") as f:
        json.dump(data, f)

def consent(title, yes):
    text = "[oui;NON]"
    if yes:
      text = "[OUI;non]"

    s = inputStr(title + " " + text)

    if len(s) == 0:
        return yes

    return s.upper() == 'OUI'



