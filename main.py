import json
import os

FILE = "data.json"  # chemin vers le fichier de données


def main():
    """Boucle principale du programme"""

    running = True
    while running:  # tant que running == True rester dans le programme
        printHelp()  # affiche les différents choix
        command = inputInt("Entrez votre choix: ")  # demande à l'utilisateur son choix
        if command == 0:  # si le choix est 0 (sortie du programme)
            running = False  # sortir de la boucle
            stop()  # fonction pour sortir du programme
        elif command == 1:  # si le choix est 1 (ajout d'un contact)
            add()  # fonction pour ajouter un nouveau contact
        elif command == 2:  # si le choix est 2 (recherche d'un contact)
            get()  # fonction pour récupérer un contact
        elif command == 3:  # si le choix est 3 (suppression d'un contact)
            delete()  # fonction pour supprimer un contact


def stop():
    """Fonction pour sortir du programme"""
    print("Bye bye !")  # affiche le message d'au revoir


def add():
    """Fonction pour ajouter un nouveau contact"""

    while True:
        name = inputStr("Nom (0 pour terminer): ")  # demande le nom du nouveau contact
        if name == '0':  # si le nom est '0' alors sortir de la boucle infinie
            break

        if exist(name):  # si le nom existe déjà alors afficher le message d'erreur et revenir au début de la boucle
            print("Erreur: ce nom est déjà enregistré !")
            continue

        num = inputPhoneNumber("Numéro de téléphone: ")  # demande le numéro de téléphone
        if num is None:  # si le numéro est None alors afficher le message d'erreur et revenir au début de la boucle
            print("Erreur: le numéro de téléphone n'est pas valide !")
            continue

        addContact(name, num)  # ajouter le contact
        print("Le contact " + name + " a bien été enregistré")  # afficher le message qui valide le contact


def get():
    """Fonction pour récupérer un contact"""

    while True:
        name = inputStr("Nom (0 pour terminer): ")  # demande le nom du contact
        if name == '0':  # si le nom est '0' alors sortir de la boucle infinie
            break

        result = getContact(name)  # recherche le numéro du contact

        if result is None:  # si le résultat est nul alors afficher le message d'erreur et revenir au début de la boucle
            print("Erreur: aucun numéro associé à " + name + " !")
            continue

        print("Le numéro de téléphone de " + name + " est: " + result)  # afficher le numéro de téléphone
        return  # quitter la boucle et la fonction


def delete():
    """Fonction pour supprimer un contact"""

    while True:
        name = inputStr("Nom (0 pour terminer): ")  # demande le nom du contact
        if name == '0':  # si le nom est '0' alors sortir de la boucle infinie
            break

        if not exist(name):  # si le contact n'existe pas alors
            print("Erreur: " + name + " n'existe pas !")  # afficher le message d'erreur
            continue  # revenir au début de la boucle

        if not consent("Êtes-vous sûr de vouloir supprimer "+name+" ?", True):  # si l'utilisateur n'est pas consentant
            print("[ACTION_ANNULÉ]")  # afficher le message d'erreur
            continue  # revenir au début de la boucle

        delContact(name)  # supprime le contact
        print(name + " a bien été supprimé(e)")  # affiche le message qui valide la suppression
        return  # quitter la boucle et la fonction


def exist(name):
    """Renvoie True si le contact est déjà enregistré"""
    return index(name) is not None  # renvoie True si le contact n'est pas None


def index(name):
    """
    Renvoie les données du contact\n
    {'name': '$name', 'number': '$number'}
    """
    content = getFile()  # récupère le fichier
    for i in content:  # pour tous les contacts
        if i['name'].upper() == name.upper():  # si le nom (en maj) correspond au nom demandé (en maj)
            return i  # renvoyer le contact


def addContact(name, number):
    """Ajoute le contact"""
    content = getFile()  # récupère le contenu du fichier

    content.append({"name": name, "number": number})  # ajoute le nouveau contact (format json)
    writeFile(content)  # écrit le fichier avec le nouveau contact


def getContact(name):
    """Récupère le numéro du contact"""
    i = index(name)  # récupère le contact
    if i is not None:  # si le contact existe alors renvoyer le numéro
        return i['number']


def delContact(name):
    """Supprime le contact"""
    i = index(name)  # récupère le contact
    if i is None:  # si le contact n'existe pas, sortir de la fonction
        return

    content = getFile()  # récupère l'intégralité des contacts

    content.remove(i)  # supprime le contact
    writeFile(content)  # écrit le fichier sans le contact


#                                   #-----****-----#                                   #

def inputInt(*title):
    """Fonction qui permet d'input un integer"""
    try:
        return int(inputValue(title))  # converti en int la valeur d'entrée
    except ValueError:  # si la valeur d'entrée n'est pas un int, sortir de la fonction
        pass


def inputStr(*title):
    """Fonction qui permet d'input un string"""
    try:
        return str(inputValue(title))  # converti en str la valeur d'entrée
    except ValueError:  # si la valeur d'entrée n'est pas un str, sortir de la fonction
        pass


def inputPhoneNumber(*title):
    """Fonction qui permet d'input un phone number"""
    inp = inputInt(title)  # input le numéro de téléphone (int) pour vérifier que tous les caractères sont des chiffres
    if inp is None:  # si le numéro est None alors ne rien renvoyer
        return

    inp = str(inp)  # conversion du numéro (int) en str
    inp = '0' + inp  # ajout du premier zéro qui a disparu, car pour un int tous les zéros inutiles sont supprimés

    if len(inp) != 10:  # si le numéro ne contient pas 10 chiffres alors ne rien renvoyer
        return

    return inp  # renvoyer le numéro de téléphone en str


def inputValue(title):
    """Fonction qui permet d'input une valeur"""

    while type(title) == tuple:  # si le paramètre est un tuple, en extraire le premier str
        if len(title) != 0:
            title = title[0]
        else:
            title = ""
            break

    return input(title)  # input text


def getFile():
    """Récupère le contenu du fichier"""
    if empty():  # si le fichier est vide ou n'existe pas, l'initialiser
        default()

    with open(FILE, "r") as f:
        return json.load(f)  # renvoie le contenu json du fichier


def empty():
    """Renvoi True si le répertoire est vide"""
    if not os.path.exists(FILE):  # si le fichier n'existe pas, le créer et l'initialiser
        default()

    with open(FILE, "r") as f:
        return len(f.read()) == 0  # renvoie True si la taille du contenu du fichier est 0


def default():
    """Fonction qui crée le fichier (s'il n'existe pas) et l'initialise"""
    with open(FILE, "w") as f:
        json.dump([], f)  # crée un tableau vide dans le fichier json
    f.close()  # ferme le fichier après utilisation


def writeFile(data):
    """Écrit le contenu du fichier"""
    with open(FILE, "w") as f:
        json.dump(data, f)  # remplace le contenu du fichier par 'data'
    f.close()  # ferme le fichier après utilisation


def consent(title, yes):
    """Renvoie True si l'utilisateur consent à l'action sinon False"""

    text = "[oui;NON]"
    if yes:  # si oui est la réponse par défaut
        text = "[OUI;non]"

    s = inputStr(title + " " + text)  # demande un str à l'utilisateur

    if len(s) == 0:  # si l'entrée est vide alors renvoyer la valeur par défaut
        return yes

    return s.upper() == 'OUI'  # renvoie True si l'entrée (en maj) est "OUI"


def printHelp():
    """Fonction qui affiche les différents choix"""

    print("_________________________________")
    print("|0-quitter                      |")
    print("|1-écrire dans le répertoire    |")
    print("|2-rechercher dans le répertoire|")
    print("|3-supprimer dans le répertoire |")
    print("\_______________________________/\n")


main()  # lance la fonction principale du programme
