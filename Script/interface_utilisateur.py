"""
Import des modules :
    os = communiquer avec os
    consolemenu = creer des menus et sous-menu
"""
import os
from consolemenu import *
from consolemenu.menu_component import Dimension


###############################################################################
###############################################################################
# VAR de base pour le script client :

# Variable qui va principalement nous servir pour communiquer la demande du client au serveur
client_move = [None]

# client_move contiendra toujours 2 valeurs. Le premier sous-menu choisi par le client et enfin la demande choisie par le client
# Exemple client_move = [6, 2] le client est dans le menu info system et veut afficher l'heure de démarrage

# Variable pour les menus et sous-menu

# Option de retour en arrière sous forme de variable pour éviter les répétitions
prec = "Page Précédente"

# Menu principale

liste_main = ["CPU",
              "Disk(s)",
              "Mémoire",
              "Réseau",
              "Manageur de process",
              "Capteur (température,etc..)",
              "Informations systèmes"
              ]

# sous-menu CPU
liste_menu0 = ["Utilisation du CPU",
               "Fréquence du CPU ",
               "Nombre de CPU", 
               "CPU time",
               "Statistiques sur le(s) CPU",
               prec
               ]

# sous-menu DISK
liste_menu1 = ["Informations sur les partitions",
               "Informations sur l'utilisation du disk(s) ",
               "Informations sur les disk(s)",
               prec
               ]

# sous-menu MEMOIRE
liste_menu2 = ["Mémoire ram Utilisée",
               "Mémoire ram Totale ",
               "Mémoire ram Utilisée en % ",
               "Récap complet avec le swap en plus",
               prec
               ]

# sous-menu NETWORK
liste_menu3 = ["Statistiques d'E/S réseau",
               "Connexions des sockets",
               "Adresses associées à chaque carte d'interface réseau",
               "Net Stat",
               "Informations sur chaque carte d'interface réseau",
               prec
               ]

# sous-menu PROCESS
liste_menu4 = ["Liste des Processus",
               prec
               ]

# sous-menu CAPTEUR
liste_menu5 = ["Température",
               "Ventilateur",
               "Batterie",
               prec
               ]

# sous-menu INFO SYS
liste_menu6 = ["Informations des Utilisateurs",
               "Heure d'allumage",
               prec
               ]

# Tubes
#Vérifie si le tube nommé "/tmp/tube_client_to_serveur" existe et l'ouvre s'il existe
if os.path.exists("/tmp/tube_client_to_serveur"):
    fd_w = os.open("/tmp/tube_client_to_serveur", os.O_WRONLY)
else:
    print("Le Serveur n'est pas Allumer")
    exit()
    
    
#Vérifie si le tube nommé "/tmp/tube_serveur_to_client" existe et l'ouvre s'il existe
if os.path.exists("/tmp/tube_serveur_to_client"):
    fd_r = os.open("/tmp/tube_serveur_to_client", os.O_RDONLY)     
else:
    print("Le Serveur n'est pas Allumer")
    exit()


###############################################################################
###############################################################################
# Choix des pages :


def main():
    global client_move, main_format     # Met les variables à l'état global dans les menus du client et du format pour les menus
    client_move = [0, 0]                # Retour à la case départ pour le client
    main_format = MenuFormatBuilder().set_prompt("Choix_Sélectionner_>")    # Format pour tous les menus
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Le commentaire en dessous du titre,
    # Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_main, "Boite à Outils professionnels :", "Choisissez le Menu souhaiter !",
                         exit_option_text='Quitter la Boite à Outils', formatter=main_format)
    menu.show()     # Affiche le menu
    menu.join()     # Connect tous les éléments au menu
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move[0] = select         # La première valeur de client_move récupère le menu sélectionné par l'utilisateur
    if select == 0:
        # CPU
        menu0()
    elif select == 1:
        # DISK
        menu1()
    elif select == 2:
        # MEMOIRE
        menu2()
    elif select == 3:
        # NETWORK
        menu3()
    elif select == 4:
        # PROCESS
        menu4()
    elif select == 5:
        # CAPTEUR
        menu5()
    elif select == 6:
        # INFO SYS
        menu6()
    else:
        exit()


###############################################################################
###############################################################################
# Les différentes pages :


def menu0():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu0, "Menu CPU :", exit_option_text='Quitter la Boite à Outils', formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 5:                 # Retour en arrière
        main()
    elif select == 6:               # Quitte le script client
        exit()
    else:
        demande()           # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


def menu1():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu1, "Menu Disk(s) :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 3:                 # Retour en arrière
        main()
    elif select == 4:               # Quitte le script client
        exit()
    else:
        demande()          # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


def menu2():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu2, "Menu Mémoire :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 4:                 # Retour en arrière
        main()
    elif select == 5:               # Quitte le script client
        exit()
    else:
        demande()       # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


def menu3():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu3, "Menu Réseau :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 5:                 # Retour en arrière
        main()
    elif select == 6:               # Quitte le script client
        exit()
    else:
        demande()      # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


def menu4():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu4, "Menu des Process :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 1:                 # Retour en arrière
        main()
    elif select == 2:               # Quitte le script client
        exit()
    else:
        demande()       # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


def menu5():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu5, "Menu Capteur :", "NE FONCTIONNE PAS DANS UNE VM CAR UNE VM NA PAS DE CAPTEUR",
                         exit_option_text='Quitter la Boite à Outils', formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 3:                 # Retour en arrière
        main()
    elif select == 4:               # Quitte le script client
        exit()
    else:
        demande()       # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


def menu6():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu,
    # Nom pour le choix de sortie du menu ou sous-menu,
    # Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu6,
                         "Menu Information systèmes :",
                         exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajoute dans la liste le sous-menu sélectionné
    if select == 2:                 # Retour en arrière
        main()
    elif select == 3:                 # Quitte le script client
        exit()
    else:
        demande()      # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoit la demande au serveur


###############################################################################
###############################################################################
# Page de résultat :


def menu_result(result):
    y = result.split("\n")
    liste_longueur = []
    for phrase in y:
        longueur = len(phrase)
        liste_longueur.append(longueur)
    max_r = max(liste_longueur)
    max_r += 20
    precedant = ["Page Précédente"]             # Variable pour menu_result
    thin = Dimension(width=max_r, height=40)      # Ajustement de la taille du menu pour menu_result
    # Configuration du format pour menu_result
    menu_format = MenuFormatBuilder(max_dimension=thin).set_prompt("Choix_Sélectionner_>")  
    menu = SelectionMenu(precedant,
                         "Résultat de la demande :",
                         result, exit_option_text='Quitter la Boite à Outils',
                         formatter=menu_format)
    menu.show()
    menu.join()
    select = menu.selected_option       # Récupère la valeur sélectionnée par le client
    return select                       # Renvoi la valeur sélectionnée par le client


###############################################################################
###############################################################################
# Fonction demande :

def demande():
    menu = client_move[0]           # Récupère le menu précédent pour le renvoyer dedans à la fin de l'affichage du résultat
    result = Tube()                 # Lance la demande du client au serveur. Récupère le résultat dans la variable result
    select = menu_result(result)    # Envoi le résultat dans menu_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        if menu == 0:
            # CPU
            menu0()
        elif menu == 1:
            # DISK
            menu1()
        elif menu == 2:
            # MEMOIRE
            menu2()
        elif menu == 3:
            # NETWORK
            menu3()
        elif menu == 4:
            # PROCESS
            menu4()
        elif menu == 5:
            # CAPTEUR
            menu5()
        elif menu == 6:
            # INFO SYS
            menu6()
    else:
        exit()


###############################################################################
###############################################################################
# Fonction tube :


# Définit une fonction nommée "Tube" qui ne prend en entrée aucun argument
def Tube():
    # Encode la chaîne de caractères (formée par la concaténation des éléments "client_move[0]" et "client_move[1]" séparés par un ":") en utilisant l'encodage utf-8
    # et le stock dans la variable "line"
    line = str.encode((str(client_move[0]) + ":" + str(client_move[1])))
    # Écrit les données de la variable "line" dans le tube nommé "fd_w"
    os.write(fd_w, line)
    # Lit jusqu'à 15000 octets de données à partir du tube nommé "fd_r" et les stocks dans la variable "result"
    result = os.read(fd_r, 15000)
    # Décode les données de la variable "result" en utilisant l'encodage utf-8
    result = result.decode("utf-8")
    # Retourne la valeur de la variable "result" lorsque la fonction est appelée
    return result


###############################################################################
###############################################################################
# INIT

if __name__ == "__main__":
    main()
