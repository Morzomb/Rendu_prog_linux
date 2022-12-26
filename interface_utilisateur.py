import os                                           # Module pour communiquer avec os
from consolemenu import *                           # Module qui créée des menus et sous-menu avec plein d'options déjà existant
from consolemenu.menu_component import Dimension


########################################################################################################################
########################################################################################################################
# VAR de base pour le script client :

client_move = [None]    # Variable qui va principalement nous servir pour communiquer la demande du client au serveur

# client_move contiendra toujours 2 valeurs en premier, le premier menu choisi par le client et enfin le sous-menu choisi
# Exemple client_move = [6, 2] le client est dans le menu info system et veut afficher l'heure de démarrage

# Variable pour les menus et sous-menu

prec = "Page Précédente"   # Option de retour en arrière sous forme de variable pour éviter les répétitions 

# Menu principale 

liste_main = ["CPU", "Disk(s) ", "Mémoire", "Réseau", "Manageur de process", "Capteur (température,etc..)",
              "Information systèmes"]
              
# sous-menu CPU 
liste_menu0 = ["Utilisation du CPU", "Fréquence du CPU ", "Nombre de CPU", "CPU time", "Statistic sur le(s) CPU",
               prec]

# sous-menu DISK 
liste_menu1 = ["Information sur les partitions", "Information sur l'utilisation du disk(s) ",
               "Information sur les disk(s)", prec]

# sous-menu MEMOIRE 
liste_menu2 = ["Mémoire ram Utiliser", "Mémoire ram Total ", "Mémoire ram Utiliser en % ",
               "Récap complet avec le swap en plus", prec]
               
# sous-menu NETWORK 
liste_menu3 = ["net0", "net1", "net2", "Net Stat", "net4", prec]

# sous-menu PROCESS 
liste_menu4 = ["Liste des Processus", prec]

# sous-menu CAPTEUR 
liste_menu5 = ["Température", "Ventilateur", "Batterie", prec]

# sous-menu INFO SYS 
liste_menu6 = ["Information des Utilisateurs", "Heure d'allumage ", prec]

# Tubes
fd_w = os.open("/tmp/tube_client_to_serveur", os.O_WRONLY)

fd_r = os.open("/tmp/tube_serveur_to_client", os.O_RDONLY)


########################################################################################################################
########################################################################################################################
# Choix des pages :


def main():
    global client_move, main_format     # Mise en global les movements dans les menus du client et du format pour les menus 
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
    if select == 1:
        # DISK
        menu1()
    if select == 2:
        # MEMOIRE
        menu2()
    if select == 3:
        # NETWORK
        menu3()
    if select == 4:
        # PROCESS
        menu4()
    if select == 5:
        # CAPTEUR
        menu5()
    if select == 6:
        # INFO SYS
        menu6()


########################################################################################################################
########################################################################################################################
# Les différentes pages :


def menu0():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu0, "Menu CPU :", exit_option_text='Quitter la Boite à Outils', formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 5:                 # Retour en arrière
        main()
    elif select == 6:               # Quitter le script client
        exit()
    else:
        cpu()           # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


def menu1():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu1, "Menu Disk(s) :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 3:                 # Retour en arrière
        main()
    elif select == 4:               # Quitter le script client
        exit()
    else:
        disk()          # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


def menu2():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu2, "Menu Mémoire :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 4:                 # Retour en arrière
        main()
    elif select == 5:               # Quitter le script client
        exit()
    else:
        memoire()       # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


def menu3():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu3, "Menu Réseau :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 5:                 # Retour en arrière
        main()
    elif select == 6:               # Quitter le script client
        exit()
    else:
        networks()      # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


def menu4():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu4, "Menu des Process :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 1:                 # Retour en arrière
        main()
    elif select == 2:               # Quitter le script client
        exit()
    else:
        process()       # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


def menu5():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu5, "Menu Capteur :", "NE FONCTIONNE PAS DANS UNE VM CAR UNE VM NA PAS DE CAPTEUR",
                         exit_option_text='Quitter la Boite à Outils', formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 3:                 # Retour en arrière
        main()
    elif select == 4:               # Quitter le script client
        exit()
    else:
        capteur()       # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


def menu6():
    global client_move              # client_move est rendu global pour qu'elle soit tout le temps à jour
    del client_move[1]              # Suppression du sous-menu
    # SelectionMenu (Listes des noms des choix, Le Titre afficher pour le menu, Nom pour le choix de sortie du menu ou sous-menu, Enfin import du format à respecter pour le menu ou sous-menu)
    menu = SelectionMenu(liste_menu6, "Menu Information systèmes :", exit_option_text='Quitter la Boite à Outils',
                         formatter=main_format)
    menu.show()
    menu.join()
    select = menu.selected_option   # Récupère la valeur sélectionnée par le client
    client_move.append(select)      # client_move ajout dans la liste le sous-menu sélectionner
    if select == 2:                 # Retour en arrière
        main()
    if select == 3:                 # Quitter le script client
        exit()
    else:
        sys_info()      # Si le choix n'est ni retour arrière ni quitter lance la fonction qui envoi la demande au serveur


########################################################################################################################
########################################################################################################################
# Page de résultat :


def page_result(result):
    precedant = ["Page Précédente"]             # Variable pour la page_result
    thin = Dimension(width=120, height=40)      # Ajustement de la taille du menu pour la page_result
    menu_format = MenuFormatBuilder(max_dimension=thin).set_prompt("Choix_Sélectionner_>")  # Configuration du format pour la page_result
    menu = SelectionMenu(precedant, "Résultat de la demande :", result, exit_option_text='Quitter la Boite à Outils',
                         formatter=menu_format)
    menu.show()
    menu.join()
    select = menu.selected_option       # Récupère la valeur sélectionnée par le client
    return select                       # Renvoi la valeur sélectionné par le client


########################################################################################################################
########################################################################################################################
# Fonction tube :


# Définit une fonction nommée "Tube" qui prend en entrée aucun argument
def Tube():
    # Encode la chaîne de caractères (formée par la concaténation des éléments "client_move[0]" et "client_move[1]" séparés par un ":") en utilisant l'encodage utf-8 et la stock dans la variable "line"
    line = str.encode((str(client_move[0]) + ":" + str(client_move[1])))
    # Écrit les données de la variable "line" dans le tube nommé "fd_w"
    os.write(fd_w, line)
    # Lit jusqu'à 15000 octets de données à partir du tube nommé "fd_r" et les stocks dans la variable "result"
    result = os.read(fd_r, 15000)
    # Décode les données de la variable "result" en utilisant l'encodage utf-8
    result = result.decode("utf-8")
    # Retourne la valeur de la variable "result" lorsque la fonction est appelée
    return result


########################################################################################################################
########################################################################################################################
# Fonction disk(s) :


def cpu():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu0()


########################################################################################################################
########################################################################################################################
# Fonction disk(s) :


def disk():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu1()


########################################################################################################################
########################################################################################################################
# Fonction memoire :


def memoire():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu2()


########################################################################################################################
########################################################################################################################
# Fonction networks :


def networks():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu3()


########################################################################################################################
########################################################################################################################
# Fonction networks :


def process():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu4()


########################################################################################################################
########################################################################################################################
# Fonction capteur :


def capteur():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu5()


########################################################################################################################
########################################################################################################################
# Fonction sys_info :


def sys_info():
    result = Tube()                 # Lance la demande du client au serveur récupère le résultat dans la variable result
    select = page_result(result)    # Envoi le résultat dans page_result pour l'afficher proprement
    if select == 0:                 # Si select = 0 retour à la page de sous-menu Précédente
        menu6()


########################################################################################################################
########################################################################################################################
# INIT

if __name__ == "__main__":
    main()
