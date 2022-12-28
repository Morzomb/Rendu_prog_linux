"""
Import des modules :
    datetime = la date et heure
    sys = communiquer avec le system
    psutil = récupération des informations sur le system
    socket = récupération des informations réseaux
    os = communiquer avec os
    bytes2human = convertie les informations en un format lisible
    signal = permet la recuperation de sortie du programme
"""
import datetime
import sys
import psutil
import socket
import os
from psutil._common import bytes2human
import signal


# Toutes les fonctions pour les demandes du client classées par type de demande :

###############################################################################
###############################################################################
# Fonction pour toutes les demandes CPU :


# Fonction qui est appelée avec le variable item qui diffère selon le choix de l'utilisateur
def cpu(item):
    try:
        if item == 0:
            cpu_usage = psutil.cpu_percent(interval=0.5)  # Recuperation du pourcentage d'utilisation du CPU
            result = (
                "Utilisation du CPU : {} %".format(cpu_usage))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        elif item == 1:
            cpu_frequence = psutil.cpu_freq().current
            result = ("Fréquence du CPU : {} MHz".format(
                cpu_frequence))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        elif item == 2:
            nombre_cpu = psutil.cpu_count()
            result = f"Nombre de CPU : {nombre_cpu}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        elif item == 3:
            # Définit le format de chaîne de caractères à utiliser pour afficher les informations de temps de CPU
            fmt = "| {:>5s}| {:>5s}| {:>6s}| {:>5s}| {:>7s}| {:>5s}| {:>7s}| {:>5s}| {:>5s}| {:>10s}|"

            # Crée une chaîne de caractères contenant les titres des colonnes à afficher
            titre = fmt.format("USER", "NICE", "SYSTEM", "IDLE", "IOWAIT", "IRQ", "SOFTIRQ", "STEAL", "GUEST",
                               "GUEST_NICE")

            # Appelle la fonction cpu_times_percent() de psutil pour obtenir les informations de temps de CPU du système
            # L'argument interval indique la période de temps à utiliser pour calculer les pourcentages de temps de CPU
            # L'argument percpu indique si les informations doivent être obtenues
            # pour chaque CPU individuellement ou pour l'ensemble du système
            cpu_time = psutil.cpu_times_percent(interval=1, percpu=False)

            # Mise en forme de la réponse à envoyer à l'utilisateur
            result = titre
            d_info = fmt.format(
                str(cpu_time.user),
                str(cpu_time.nice),
                str(cpu_time.system),
                str(cpu_time.idle),
                str(cpu_time.guest_nice),
                str(cpu_time.iowait),
                str(cpu_time.softirq),
                str(cpu_time.steal),
                str(cpu_time.guest),
                str(cpu_time.guest_nice)
            )
            result = result + "\n" + d_info

            # Crée une chaîne de caractères contenant le titre "CPU time" et les valeurs de temps de CPU
            result = f"CPU time :\n{result}"

            # Renvoie le résultat pour l'envoyer
            return result
        elif item == 4:
            # Définit le format de chaîne de caractères à utiliser pour afficher les informations de statistiques de CPU
            fmt = "| {:>12s}| {:>10s}| {:>15s}| {:>8s}|"

            # Crée une chaîne de caractères contenant les titres des colonnes à afficher
            titre = fmt.format("CTX_SWITCHES", "INTERRUPTS", "SOFT_INTERRUPTS", "SYSCALLS")

            # Appelle la fonction cpu_stats() de psutil pour obtenir les informations de statistiques de CPU du système
            cpu_stat = psutil.cpu_stats()

            # Mise en forme de la réponse à envoyer à l'utilisateur
            result = titre
            d_info = fmt.format(
                str(cpu_stat.ctx_switches),
                str(cpu_stat.interrupts),
                str(cpu_stat.soft_interrupts),
                str(cpu_stat.syscalls)
            )
            result = result + "\n" + d_info
            result = f"Statistic sur le CPU :\n{result}"

            # Renvoi le résultat pour l'envoyer
            return result

    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


###############################################################################
###############################################################################
# Fonction pour toutes les demandes de(s) disk(s) :


def disk(item):
    try:
        if item == 0:
            # Appelle la fonction disk_partitions() de psutil
            # pour obtenir les informations sur les partitions de disque du système
            # L'argument all indique si toutes les partitions doivent
            # être incluses ou seulement celles qui sont montées
            partitions_disk = psutil.disk_partitions(all=True)

            # Définit le format de chaîne de caractères à utiliser
            # pour afficher les informations sur les partitions de disque
            fmt = "| {:>12s}| {:>24s}| {:>12s}| {:>7s}| {:>7s}|"

            # Crée une chaîne de caractères contenant les titres des colonnes à afficher
            titre = fmt.format("DEVICE", "MOUNTPOINT", "FSTYPE", "MAXFILE", "MAXPATH")
            dd_info = titre

            # Parcours les informations sur les partitions de disque
            for key in partitions_disk:
                # Crée une chaîne de caractères contenant les informations sur une partition de disque
                d_info = fmt.format(
                    str(key.device),
                    str(key.mountpoint),
                    str(key.fstype),
                    str(key.maxfile),
                    str(key.maxpath)
                )

                # Ajoute les informations sur la partition de disque dans la variable dd_info
                dd_info = dd_info + "\n" + d_info

            # Mise en forme de la réponse à envoyer à l'utilisateur
            result = f"Information sur l'utilisation du disk(s) :\n{dd_info}"

            # Renvoie le résultat pour l'envoyer
            return result

        elif item == 1:
            # Chaîne de formatage pour afficher les informations sur l'utilisation du disque de manière alignée
            fmt = "| {:<20s}| {:>8s}| {:>8s}| {:>8s}| {:>8s}%| {:8s}| {:10s}|"
            # Création de l'en-tête du tableau en utilisant la chaîne de formatage
            titre = fmt.format("DEVICE", "TOTAL", "UTIL.", "LIBRE", "% UTIL", "TYPE",
                               "MONTAGE")
            for part in psutil.disk_partitions():  # Pour chaque partition du disque
                # Récupère les informations sur l'utilisation de la partition
                # en utilisant la méthode disk_usage de la bibliothèque psutil
                usage = psutil.disk_usage(
                    part.mountpoint)
                d_info = fmt.format(
                    # Récupère les informations sur l'utilisation du disque en utilisant la chaîne de formatage
                    part.device,  # Nom du périphérique
                    bytes2human(usage.total),  # Taille totale du périphérique
                    bytes2human(usage.used),  # Taille utilisée sur le périphérique
                    bytes2human(usage.free),  # Taille libre sur le périphérique
                    str(int(usage.percent)),  # Pourcentage d'utilisation du périphérique
                    part.fstype,  # Type de système de fichiers du périphérique
                    part.mountpoint  # Emplacement du montage du périphérique
                )
                # Ajoute l'en-tête et les informations sur l'utilisation du disque dans une chaîne de caractères
                d_info = titre + "\n" + d_info
            # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            result = f"Information sur l'utilisation du disk(s) :\n{d_info}"
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 2:
            information_disk = psutil.disk_io_counters(perdisk=True)
            # Définit le format de chaîne de caractères à utiliser pour afficher les informations d'E/S de disque
            fmt = "| {:>4s}| {:>10s}| {:>11s}| {:>10s}| {:>11s}| {:>9s}| {:>10s}| {:>17s}| {:>18s}| {:>9s}|"

            # Crée une chaîne de caractères contenant les titres des colonnes à afficher
            titre = fmt.format("DISK", "READ_COUNT", "WRITE_COUNT", "READ_BYTES", "WRITE_BYTES", "READ_TIME",
                               "WRITE_TIME", "READ_MERGED_COUNT", "WRITE_MERGED_COUNT", "BUSY_TIME")

            # Initialise une chaîne de caractères vide pour stocker les informations d'E/S de disque
            dd_info = titre

            # Parcours les informations d'E/S de disque
            for key in information_disk:
                # Obtient les informations d'E/S de disque pour chaque disque
                part = psutil.disk_io_counters(perdisk=True)[key]

                # Crée une chaîne de caractères contenant les informations d'E/S de disque pour chaque disque
                d_info = fmt.format(
                    key,
                    str(part.read_count),
                    str(part.write_count),
                    str(part.read_bytes),
                    str(part.write_bytes),
                    str(part.read_time),
                    str(part.write_time),
                    str(part.read_merged_count),
                    str(part.write_merged_count),
                    str(part.busy_time)
                )

                # Ajoute les informations d'E/S de disque à la chaîne de caractères des informations d'E/S de disque
                dd_info = dd_info + "\n" + d_info

            # Mise en forme de la réponse à envoyer à l'utilisateur
            result = f"Informations sur les disk(s) :\n{dd_info}"

            # Renvoie le résultat pour l'envoyer
            return result

    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


###############################################################################
###############################################################################
# Fonction pour toutes les demandes memoire :


def memoire(item):
    try:
        if item == 0:
            # On calcule l'espace de mémoire vive utilisé en soustrayant
            # l'espace de mémoire vive disponible de l'espace total de mémoire vive
            mem_utiliser = psutil.virtual_memory().total - psutil.virtual_memory().available

            # On formate la valeur de l'espace de mémoire vive utilisé en chaîne de caractères
            result = ("Mémoire ram utilisée : {}".format(int(mem_utiliser / 1024 / 1024)))
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 1:
            # On récupère l'espace total de mémoire vive
            mem_total = psutil.virtual_memory().total
            # On formate la valeur de l'espace total de mémoire vive en chaîne de caractères
            # en divisant la valeur par 1024 puis par 1024 pour la convertir en Mo
            result = ("Mémoire ram totale : {}".format(int(mem_total / 1024 / 1024)))
            # On renvoie le résultat sous forme de chaîne de caractères
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 2:
            # On récupère l'utilisation de la mémoire vive en pourcentage
            mem_utilisation_pourcen = psutil.virtual_memory().percent
            # On formate la valeur de l'utilisation de la mémoire vive en chaîne de caractères
            # en utilisant la fonction "format" pour inclure la valeur dans la chaîne de caractères
            result = ("Mémoire ram utilisée en % : {}".format(int(mem_utilisation_pourcen)))
            # Mise en Forme de la réponse à envoyer à l'utilisateur
            # On renvoie le résultat sous forme de chaîne de caractères
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 3:
            # On récupère les informations sur l'utilisation de la mémoire vive
            # et de la mémoire virtuelle (swap) sous forme de listes de chaînes de caractères formatées
            mem = fmt_ntuple(psutil.virtual_memory())
            swp = fmt_ntuple(psutil.swap_memory())
            # On calcule la longueur maximale des listes
            mx = max(len(mem), len(swp))
            # On ajoute des chaînes vides à chaque liste pour avoir la même longueur
            mem += [" " * 20] * mx
            swp += [" " * 20] * mx
            # On crée la chaîne de caractères qui va servir d'en-tête pour le résultat final
            result = "Memory".center(20) + ' | ' + "Swap".center(20) + ' |'
            # On parcourt les éléments de chaque liste et on concatène les chaînes de caractères
            # en ajoutant des séparateurs " | " entre chaque élément
            for x in range(0, mx):
                result = result + "\n" + mem[x] + ' | ' + swp[x] + ' |'
            return result  # Renvoie le résultat pour l'envoyer

    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))

def fmt_ntuple(nt):
    # Initialisation d'une liste vide pour stocker les chaînes de caractères formatées
    r = []
    # Pour chaque champ (attribut) de l'objet "nt"
    for name in nt._fields:
        # On récupère la valeur de ce champ
        valeur = getattr(nt, name)
        # Si le nom du champ est différent de "percent",
        # on formate la valeur en utilisant la fonction "bytes2human"
        if name != 'percent':
            valeur = bytes2human(valeur)
        # Sinon, on formate la valeur en pourcentage avec 2 chiffres après la virgule
        else:
            valeur = "{:5.2f}%".format(valeur)
        # On ajoute la chaîne de caractères formatée à la liste "r"
        r.append("{:10s} : {:>7s}".format(name.capitalize(), valeur))
    # On renvoie la liste "r" en sortie de la fonction
    return r


###############################################################################
###############################################################################
# Fonction pour toutes les demandes networks :


def networks(item):
    try:
        if item == 0:
            '''
            Renvoie les statistiques d'E/S réseau à l'échelle du système
            sous la forme d'un tuple nommé comprenant les attributs suivants :
            '''
            # On récupère les informations sur l'utilisation des interfaces réseau
            net0 = psutil.net_io_counters(pernic=True)
            # On définit le format de chaîne de caractères qui va servir à formater les informations
            # pour chaque interface réseau
            fmt = "| {:>5s}| {:>11s}| {:>8s}| {:>14s}| {:>11s}| {:>20s}| {:>20s}|"
            # On crée la chaîne de caractères qui va servir d'en-tête pour le résultat final
            titre = fmt.format("CARTE", "BIT ENVOYER", "BIT REÇU", "PACKET ENVOYER", "PACKET REÇU",
                               "PERTE DE PAQUETS / E", "PERTE DE PAQUETS / S")
            result = titre
            # On parcourt le dictionnaire des informations sur l'utilisation des interfaces réseau
            # et on formate les informations pour chaque interface réseau
            for key in net0:
                # On récupère les informations sur l'interface réseau courante
                part = psutil.net_io_counters(pernic=True)[key]
                # On formate les informations sous forme de chaîne de caractères
                d_info = fmt.format(
                    key,
                    bytes2human(part.bytes_sent),  # Nombre de bits envoyés par l'interface réseau
                    bytes2human(part.bytes_recv),  # Nombre de bits reçus par l'interface réseau
                    str(part.packets_sent),  # Nombre de paquets envoyés par l'interface réseau
                    str(part.packets_recv),  # Nombre de paquets reçus par l'interface réseau
                    str(part.errin),  # Nombre de paquets perdus lors de la réception par l'interface réseau
                    str(part.errout)  # Nombre de paquets perdus lors de l'envoi par l'interface réseau
                )
                # On concatène la chaîne de caractères formée avec le résultat final
                result = result + "\n" + d_info
            # Mise en Forme de la réponse à envoyer à l'utilisateur
            result = f"Statistiques des cartes reseaux :\n{result}"
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 1:
            '''
            Renvoie les connexions de socket à l'échelle du système
            sous la forme d'une liste de tuples nommés.
            '''
            # On récupère les informations sur les connexions TCP en cours sur l'ordinateur
            net1 = psutil.net_connections(kind='tcp')
            # On définit le format de chaîne de caractères qui va servir à formater les informations
            # pour chaque connexion TCP
            fmt = "| {:>2s}| {:>22s}| {:>22s}| {:>34s}| {:>35s}|"
            # On crée la chaîne de caractères qui va servir d'en-tête pour le résultat final
            titre = fmt.format("FD", "FAMILLE", "TYPE", "LADDR", "RADDR")
            dd_info = titre
            # On parcourt le tableau des informations sur les connexions TCP
            for key in net1:
                # On formate les informations sous forme de chaîne de caractères
                d_info = fmt.format(
                    str(key.fd),  # Numéro du descripteur de fichier de la connexion
                    str(key.family),  # Famille de protocoles de la connexion (par exemple : socket.AF_INET pour IPv4)
                    str(key.type),  # Type de socket de la connexion (par exemple : socket.SOCK_STREAM pour TCP)
                    str(key.laddr),  # Adresse locale de la connexion (adresse IP et numéro de port)
                    str(key.raddr)  # Adresse distante de la connexion (adresse IP et numéro de port)
                )
                dd_info = dd_info + "\n" + d_info

            # On crée la chaîne de caractères qui va être renvoyée à l'utilisateur
            # en incluant l'en-tête et les informations sur chaque connexion TCP
            result = f"Les connexions de socket sont :\n{dd_info}"
            # On renvoie le résultat pour qu'il soit envoyé à l'utilisateur
            return result

        elif item == 2:
            '''
            Renvoie les adresses associées à chaque NIC (carte d'interface réseau)
            installée sur le système sous la forme d'un dictionnaire
            dont les clés sont les noms de NIC et la valeur est
            une liste de tuples nommés pour chaque adresse attribuée à la NIC.
            '''
            # Ce script utilise la bibliothèque psutil pour récupérer les informations sur les cartes réseau du système
            net2 = psutil.net_if_addrs()
            # La variable "fmt" contient une chaîne de formatage qui sera utilisée
            # pour afficher les informations de chaque carte réseau de manière formatée
            fmt = "| {:>5s}| {:>23s}| {:>29s}| {:>39s}| {:>17s}|"
            # "titre" contient les titres des colonnes qui seront affichées pour chaque carte réseau
            titre = fmt.format("CARTE", "FAMILY", "ADDRESS", "NETMASK", "BROADCAST")
            # "result" est la variable qui contiendra le résultat final à renvoyer à l'utilisateur
            result = titre
            # Pour chaque carte réseau dans la variable "net2"
            for key in net2:
                # Récupère les informations de la carte réseau dans la variable "part"
                part = psutil.net_if_addrs()[key]
                # Pour chaque entrée dans "part"
                for part2 in part:
                    # Crée une chaîne de caractères contenant les informations de la carte réseau,
                    # en utilisant le formatage défini dans "fmt"
                    d_info = fmt.format(
                        key,
                        str(part2.family),
                        str(part2.address),
                        str(part2.netmask),
                        str(part2.broadcast)
                    )
                    # Ajoute cette chaîne de caractères au résultat final
                    result = result + "\n" + d_info
            # Mise en Forme de la réponse à envoyer à l'utilisateur
            result = f"Parametres des cartes reseaux :\n{result}"
            # Renvoie le résultat pour l'envoyer
            return result

        elif item == 3:
            # Appelle la fonction "netstat" et stocke le résultat dans la variable "result"
            result = netstat()
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 4:
            """
            Renvoie des informations sur chaque NIC (carte d'interface réseau) 
            installée sur le système sous la forme d'un dictionnaire dont les clés sont les noms de NIC 
            et la valeur est un tuple nommé avec les champs suivants
            """
            # Récupère les informations sur les cartes réseau du système avec la bibliothèque psutil
            net4 = psutil.net_if_stats()
            # La variable "fmt" contient une chaîne de formatage qui sera utilisée
            # pour afficher les informations de chaque carte réseau de manière formatée
            fmt = "| {:>5s}| {:>4s}| {:>28s}| {:>5s}| {:>5s}| {:>30s}|"
            # "titre" contient les titres des colonnes qui seront affichées pour chaque carte réseau
            titre = fmt.format("CARTE", "ISUP", "DUPLEX", "SPEED", "MTU", "FLAGS")
            # "result" est la variable qui contiendra le résultat final à renvoyer à l'utilisateur
            result = titre
            # Pour chaque carte réseau dans la variable "net4"
            for key in net4:
                # Récupère les informations de la carte réseau dans la variable "part"
                part = net4[key]
                # Crée une chaîne de caractères contenant les informations de la carte réseau,
                # en utilisant le formatage défini dans "fmt"
                d_info = fmt.format(
                    key,
                    str(part.isup),
                    str(part.duplex),
                    str(part.speed),
                    str(part.mtu),
                    str(part.flags))
                # Ajoute cette chaîne de caractères au résultat final
                result = result + "\n" + d_info
            # Mise en Forme de la réponse à envoyer à l'utilisateur
            result = f"Informations des cartes reseaux :\n{result}"
            # Renvoie le résultat pour l'envoyer
            return result

    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


def resolve(ip):
    # Essaie d'exécuter le code suivant
    try:
        # Utilise la fonction "gethostbyaddr" de la bibliothèque "socket"
        # pour obtenir le nom d'hôte associé à l'adresse IP spécifiée
        data = socket.gethostbyaddr(ip)
        # Stocke le nom d'hôte dans la variable "host"
        host = data[0]
    # Si une exception est levée pendant l'exécution du code ci-dessus
    except:
        # Stocke une chaîne vide dans la variable "host"
        host = ''
    # Renvoie le nom d'hôte
    return host


def netstat():
    # Crée un dictionnaire vide nommé "proc_name"
    proc_name = {}

    # Pour chaque processus dans le système, en utilisant la bibliothèque psutil
    for p in psutil.process_iter(attrs=['pid', 'name']):
        # Ajoute l'identifiant du processus et son nom au dictionnaire "proc_name"
        proc_name[p.info['pid']] = p.info['name']

    # La variable "fmt" contient une chaîne de formatage qui sera utilisée
    # pour afficher les informations des connexions réseau de manière formatée
    fmt = "| {:>23s}| {:>23s}| {:>11s}| {:>8s}| {:>4s}|"
    # "titre" contient les titres des colonnes qui seront affichées pour chaque connexion réseau
    titre = fmt.format('LOCAL', 'DISTANCE', 'STATUS', 'PROCESS', 'HOST')

    # "r" contient un séparateur de ligne avec la même longueur que "titre"
    r = '=' * len(titre)
    # Ajoute le séparateur de ligne à "titre"
    titre = titre + "\n" + str(r)

    # Pour chaque connexion réseau du système, en utilisant la bibliothèque psutil
    for c in psutil.net_connections(kind='inet4'):
        # Stocke l'adresse et le port local de la connexion dans la variable "l"
        l = "%15s : %s" % (c.laddr[0], c.laddr[1])
        # Si l'adresse distante de la connexion est définie
        if c.raddr:
            # Stocke l'adresse et le port distant de la connexion dans la variable "r"
            r = "%15s : %s" % (c.raddr[0], c.raddr[1])
            # Appelle la fonction "resolve" en lui passant l'adresse distante de la connexion
            # en paramètre et stocke le résultat dans la variable "host"
            host = resolve(c.raddr[0])
        # Si l'adresse distante de la connexion n'est pas définie
        else:
            # Initialise la variable "r" avec une chaîne vide
            r = ""
            # Initialise la variable "host" avec une chaîne vide
            host = ""
        # Stocke le statut de la connexion dans la variable "s"
        s = c.status
        # Récupère le nom du processus associé à la connexion en utilisant l'identifiant du processus
        # et le dictionnaire "proc_name", et stocke le résultat dans la variable "p"
        p = proc_name.get(c.pid, "")
        # Ajoute une nouvelle ligne à la chaîne "titre" en utilisant la chaîne de formatage "fmt"
        # et en lui passant les valeurs de "l", "r", "s", "p" et "host" en paramètre
        titre = titre + "\n" + fmt.format(l, r, s, p, host)
    # Renvoie la chaîne "titre"
    return titre


###############################################################################
###############################################################################
# Fonction pour toutes les demandes pour les process :


def process(item):
    try:
        if item == 0:
            # Chaîne de formatage pour afficher les informations de chaque processus de manière alignée
            fmt = "| {:>5s}| {:>16s}| {:>8s}| {:>29s}|"
            # Création de l'en-tête du tableau en utilisant la chaîne de formatage
            info_p = fmt.format("PID", "UTILISATEUR", "STATUE",
                        "NOM")
            # Pour chaque processus dans la liste de processus obtenue
            # en utilisant la méthode process_iter de la bibliothèque psutil
            for proc in psutil.process_iter():
                # Récupère les informations du processus en utilisant la méthode as_dict avec les attributs spécifiés
                info = proc.as_dict(attrs=['pid', 'name', 'username','status'])
                # Ajoute les informations du processus au tableau en utilisant la chaîne de formatage
                info_p = info_p + "\n" + fmt.format(str(info.get("pid")),
                                                    str(info.get("username")),
                                                    str(info.get("status")),
                                                    str(info.get("name")))
            # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            result = f"Liste de tous les processus ouverts :\n{info_p}"
            return result  # Renvoie le résultat pour l'envoyer

    except Exception as e:  # Si une erreur est rencontrée pendant l'exécution du code
        print(str(e))  # Affiche l'erreur sous forme de chaîne de caractères


###############################################################################
###############################################################################
# Fonction pour toutes les demandes pour les capteurs :

def capteur(item):
    try:
        if item == 0:
            # Récupère les informations sur les températures
            # en utilisant la méthode sensors_temperatures de la bibliothèque psutil
            capteur_temperature = psutil.sensors_temperatures()
            # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            result = f"La température est de :\n {capteur_temperature}"
            return result  # Renvoie le résultat pour l'envoyer
        elif item == 1:
            # Récupère les informations sur les ventilateurs
            # en utilisant la méthode sensors_fans de la bibliothèque psutil
            capteur_ventilo = psutil.sensors_fans()
            # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            result = f"Informations sur les ventilateurs:\n {capteur_ventilo}"
            return result  # Renvoie le résultat pour l'envoyer
        elif item == 2:
            # Récupère les informations sur la batterie
            # en utilisant la méthode sensors_battery de la bibliothèque psutil
            capteur_batterie = psutil.sensors_battery()
            # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            result = f"Informations sur la batterie:\n {capteur_batterie}"
            return result  # Renvoie le résultat pour l'envoyer

    except Exception as e:  # Si une erreur est rencontrée pendant l'exécution du code
        print(str(e))  # Affiche l'erreur sous forme de chaîne de caractères


###############################################################################
###############################################################################
# Fonction pour toutes les demandes sys_info :


def sys_info(item):
    try:
        if item == 0:
            # Récupère les informations sur les utilisateurs en utilisant la méthode users de la bibliothèque psutil
            sys_info_user = psutil.users()
            # Chaîne de formatage pour afficher les informations de chaque utilisateur de manière alignée
            fmt = "| {:>10s}| {:>8s}| {:>17s}| {:>15s}| {:>5s}|"
            # Création de l'en-tête du tableau en utilisant la chaîne de formatage
            titre = fmt.format("NAME", "TERMINAL", "HOST", "STARTED",
                               "PID")
            result = titre  # Affectation de l'en-tête au résultat final

            for key in sys_info_user:  # Pour chaque utilisateur dans la liste d'utilisateurs
                d_info = fmt.format(  # Récupère les informations de l'utilisateur en utilisant la chaîne de formatage
                    str(key.name),  # Nom de l'utilisateur
                    str(key.terminal),  # Terminal utilisé par l'utilisateur
                    str(key.host),  # Nom de l'hôte où l'utilisateur s'est connecté
                    str(key.started),  # Heure de démarrage de la session de l'utilisateur
                    str(key.pid)  # PID du processus associé à la session de l'utilisateur
                )
                result = result + "\n" + d_info  # Ajoute les informations de l'utilisateur au tableau final
            # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            result = f"Informations sur l'utilisation du disk(s) :\n{result}"
            return result  # Renvoie le résultat pour l'envoyer

        elif item == 1:
            # Récupère l'heure de démarrage de la machine en utilisant la méthode boot_time de la bibliothèque psutil
            sys_date_h_machine = psutil.boot_time()
            result = "La machine est démarré depuis : "  # Chaîne de début de la réponse
            result = result + datetime.datetime.fromtimestamp(sys_date_h_machine).strftime(
                # Convertit l'heure de démarrage en date et heure lisible et la formate selon le format spécifié
                "%Y-%m-%d %H:%M:%S"
            )  # Mise en forme de la réponse à envoyer à l'utilisateur en utilisant la f-string
            return result  # Renvoie le résultat pour l'envoyer

    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))  # Affiche l'erreur sous forme de chaîne de caractères


###############################################################################
###############################################################################
# Fonction qui envoi tous les résultats au client :


def envoi(result):
    line = str.encode(result)  # Encode le résultat à envoyer au client
    os.write(fd_w, line)  # Écriture du résultat dans le tube
    exit()  # Le fils quit le script il est ce suicide donc


###############################################################################
###############################################################################
# Fonction suppression Tube fin de programme :


def Exit_gracefully(signal, frame):
    # Supprime les tubes nommés utilisés pour la communication entre le client et le serveur
    os.remove("/tmp/tube_client_to_serveur")
    os.remove("/tmp/tube_serveur_to_client")

    # Quitte le programme
    sys.exit(0)


###############################################################################
###############################################################################
# Fonction main :

#Appel de la fonction "Exit_gracefully" quand le signal "SIGINT" arrive. 
#Le signal SIGINT est envoyé au processus lorsqu'on appuie sur Ctrl + C dans le terminal.
signal.signal(signal.SIGINT, Exit_gracefully)

# Partie serveur récup de la demande du client
# Vérifie si le tube nommé "/tmp/tube_client_to_serveur" existe et le supprime s'il existe
if os.path.exists("/tmp/tube_client_to_serveur"):
    os.remove("/tmp/tube_client_to_serveur")

# Crée un tube nommé "/tmp/tube_client_to_serveur" avec les permissions 0o600
os.mkfifo("/tmp/tube_client_to_serveur", 0o600)

# Vérifie si le tube nommé "/tmp/tube_serveur_to_client" existe et le supprime s'il existe
if os.path.exists("/tmp/tube_serveur_to_client"):
    os.remove("/tmp/tube_serveur_to_client")

# Crée un tube nommé "/tmp/tube_serveur_to_client" avec les permissions 0o600
os.mkfifo("/tmp/tube_serveur_to_client", 0o600)

# Initialise la variable "Saisie" à une chaîne vide
Saisie = ""

# Boucle tant que "Saisie" n'est pas égale à "x"
while Saisie != "x":
    # Ouvre le tube nommé "/tmp/tube_client_to_serveur" en mode lecture seule
    fd_r = os.open("/tmp/tube_client_to_serveur", os.O_RDONLY)
    # Ouvre le tube nommé "/tmp/tube_serveur_to_client" en mode écriture seule
    fd_w = os.open("/tmp/tube_serveur_to_client", os.O_WRONLY)

    # Lit jusqu'à 100 octets de données à partir du tube nommé "/tmp/tube_client_to_serveur"
    lu = os.read(fd_r, 100)
    # Décode les données lues en utilisant l'encodage utf-8 et les stocks dans la variable "x"
    x = lu.decode("utf-8")

    # Trouve la position du premier " : " dans la chaîne de caractères "x" et le stock dans la variable "NB"
    NB = x.find(':')
    # Définit "Sous_Menu" en utilisant la sous-chaîne de caractères de "x" allant de l'indice 0 à "NB"
    Sous_Menu = x[0:NB]

    try:
        Sous_Menu = int(Sous_Menu)
        demande = x[NB + 1:]
        demande = int(demande)
        client = 1          # Client prend 1 pour la confirmation qu'un client est connecté
    except Exception as e:  # Exception pour afficher quand le client se déconnecter
        client = 0          # Client prend 0 pour indiquer qu'aucun client n'est connecté
        """print("Le client vient de quitter la session")
        exit()   # Quitte le script"""

    if client == 1:
        try:  # Debut gestion d'erreur pour le fils
            child_pid = os.fork()  # Création du Fils qui va effectuer la demande du client
        except Exception as e:  # Renvoie dans "e" l'erreur rencontré par le fils
            print("Error in fork()")
            print(str(e))
            sys.exit(-1)

        if child_pid == 0:  # seul le fils peut entrer dans ce IF
            """print("Child:  PID =", os.getpid(),     # Affiche les infos du fils pour les tests et les débogages
                  "  PPID =", os.getppid())"""
            if Sous_Menu == 0:  # Choix du Sous_Menu
                # cpu
                result = cpu(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi
            elif Sous_Menu == 1:  # Choix du Sous_Menu
                # mem
                result = disk(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi
            elif Sous_Menu == 2:  # Choix du Sous_Menu
                # disk
                result = memoire(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi
            elif Sous_Menu == 3:  # Choix du Sous_Menu
                # netw
                result = networks(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi
            elif Sous_Menu == 4:  # Choix du Sous_Menu
                # pros
                result = process(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi
            elif Sous_Menu == 5:  # Choix du Sous_Menu
                # capteur
                result = capteur(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi
            elif Sous_Menu == 6:  # Choix du Sous_Menu
                #  sysinfo
                result = sys_info(demande)  # Renvoie la demande à effectuer au menu choisie
                envoi(result)  # Renvoie le résultat à la fonction envoi

        else:
            """print("Parent: PID =", os.getpid(),  # Affiche les infos du père pour les tests et les débogages
                  "  PPID =", os.getppid(),
                  "  Child =", child_pid)"""
            os.wait()
