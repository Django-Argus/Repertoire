import json
import os

FILE = "data.json"


def main():
    """boucle principale du programme"""

    running = True
    while running:
        printHelp()
        command = inputInt("Entrez votre choix: ")
        if command == 0:
            running = False
            exit()
        elif command == 1:
            add()
        elif command == 2:
            get()
        elif command == 3:
            delete()


def exit():
    """fonction pour sortir du programme"""
    print("Bye bye !")


def add():
    """fonction pour ajouter un nouveau contact"""

    while True:
        name = inputStr("Nom (0 pour terminer): ")
        if name == '0':
            break

        if exist(name):
            print("Erreur: ce nom est déjà enregistré !")
            continue

        num = inputPhoneNumber("Numéro de téléphone: ")
        if num is None:
            print("Erreur: le numéro de téléphone n'est pas valide !")
            continue

        addContact(name, num)
        print("Le contact " + name + " a bien été enregistré")


def get():
    """fonction pour récuperer  un contact"""

    while True:
        name = inputStr("Nom (0 pour terminer): ")
        if name == '0':
            break

        result = getContact(name)

        if result is None:
            print("Erreur: aucun numéro associé à " + name + " !")
            continue

        print("Le numéro de téléphone de " + name + " est: " + result)
        return

    pass


def delete():
    """fonction pour supprimer un contact"""

    while True:
        name = inputStr("Nom (0 pour terminer): ")
        if name == '0':
            break

        if not exist(name):
            print("Erreur: " + name + " n'existe pas !")
            continue

        if not consent("Etes-vous sûr de vouloir supprimer " + name + " ?", True):
            print("[ANNULÉ]")
            continue

        delContact(name)
        print(name + " a bien été supprimé")


def exist(name):
    """renvoie True si le contact est déjà enregistré"""
    return index(name) is not None   # renvoie True si le contact n'est pas None


def index(name):
    """
    renvoie les données du contact\n
    {'name': '$name', 'number': '$number'}
    """
    content = getFile()   # récupere le fichier
    for i in content:   # pour tout les contacts si le nom (en maj) correcpond au nom demmandé (en maj) renvoyer le contact
        if i['name'].upper() == name.upper():
            return i


def addContact(name, number):
    """ajoute le contact"""
    content = getFile()   # récupere le contenu du fichier

    content.append({"name": name, "number": number})   # ajoute le nouveau contact (format json)
    writeFile(content)   # écrit le fichier avec le nouveau contact


def getContact(name):
    """récupere le numéro du contact"""
    i = index(name)   # récupere le contact
    if i is not None:   # si le contact exist alors renvoyer le numéro
        return i['number']


def delContact(name):
    """supprime le contact"""
    i = index(name)   # récupere le contact
    if i is None:   # si le contact n'exist pas sortir de la fonction
        return

    content = getFile()   # récupere l'intégralité des contacts

    content.remove(i)   # supprime le contact
    writeFile(content)   # écrit le fichier sans le contact


#                                   #-----****-----#                                   #

def inputInt(*title):
    """fonction qui permet d'input un integer"""
    try:
        return int(inputValue(title))   # converti en int la valeur d'entrée
    except ValueError:   # si la valeur d'entrée n'est pas un int sortir de la fonction
        pass


def inputStr(*title):
    """fonction qui permet d'input un string"""
    try:
        return str(inputValue(title))   # converti en str la valeur d'entrée
    except ValueError:   # si la valeur d'entrée n'est pas un int sortir de la fonction
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

    while type(title) == tuple:  # si le paramètre est un tuple en extraire le premier str
        if len(title) != 0:
            title = title[0]
        else:
            title = ""
            break

    return input(title)   #input text


def getFile():
    """recupere le contenu du fichier"""
    if empty():   # si le fichier est vide ou n'exist pas l'initialiser
        default()

    with open(FILE, "r") as f:
        return json.load(f)   # renvoie le contenu json du fichier


def empty():
    """renvoit True si le répertoire est vide"""
    if not os.path.exists(FILE):   # si le fichier n'existe pas le créer et l'initialiser
        default()

    with open(FILE, "r") as f:
        return len(f.read()) == 0   # renvoie True si la taille du contenu du fichier est 0


def default():
    """fonction qui crée le fichier (si il n'existe pas) et l'initialise"""
    with open(FILE, "w") as f:
        json.dump([], f)   # crée un tableau vide dans le fichier json
    f.close()   # ferme le fichier après utilisation


def writeFile(data):
    """ecrit le contenu du fichier"""
    with open(FILE, "w") as f:
        json.dump(data, f)   # remplace le contenu du fichier par 'data'
    f.close()   # ferme le fichier après utilisation


def consent(title, yes):
    """renvoie True si l'utilisateur concent à l'action sinon False"""

    text = "[oui;NON]"
    if yes:   # si oui est la réponse par défaut
        text = "[OUI;non]"

    s = inputStr(title + " " + text)   # demande un str a l'utilisateur

    if len(s) == 0:   # si l'entrée est vide alors renvoyer la valeur par défaut
        return yes

    return s.upper() == 'OUI'   #renvoie True si l'entrée (en maj) est "OUI"


def printHelp():
    """fonction qui affiche les différents choix"""

    print("_________________________________")
    print("|0-quitter                      |")
    print("|1-écrire dans le répertoire    |")
    print("|2-rechercher dans le répertoire|")
    print("|3-supprimer dans le répertoire |")
    print("\_______________________________/\n")


main()
