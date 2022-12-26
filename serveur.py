import datetime                             # Module pour la date et heure
import sys                                  # Module pour communiquer avec le system
import psutil                               # Module pour récupérer des informations sur le system
import socket                               # Module pour la partie réseaux
import os                                   # Module pour communiquer avec os
from psutil._common import bytes2human


# Toutes les fonctions pour les demandes du client classé par type de demande :

########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes CPU :


def cpu(item):          # Fonction qui est appelée avec le variable item qui diffère selon le choix de l'utilisateur
    try:
        if item == 0:
            cpu_usage = psutil.cpu_percent(interval=0.5)  # Recuperation du pourcentage d'utilisation du CPU
            result = (
                "Utilisation du CPU : {} %".format(cpu_usage))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result   # Renvoie le résultat pour l'envoyer
        if item == 1:
            cpu_frequence = psutil.cpu_freq().current
            result = ("Fréquence du CPU : {} MHz".format(
                cpu_frequence))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result   # Renvoie le résultat pour l'envoyer
        if item == 2:
            nombre_cpu = psutil.cpu_count()
            result = f"Nombre de CPU : {nombre_cpu}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result   # Renvoie le résultat pour l'envoyer
        if item == 3:
            cpu_time = psutil.cpu_times_percent(interval=1,
                                                percpu=False)  # Mise en Forme de la réponse à envoyer à l'utilisateur
            result = f"CPU time :\n {cpu_time}"
            return result   # Renvoie le résultat pour l'envoyer
        if item == 4:
            cpu_stat = psutil.cpu_stats()
            result = f"Statistic sur le CPU :\n {cpu_stat}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result   # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))



########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes de(s) disk(s) :


def disk(item):
    try:
        if item == 0:
            information_partition = psutil.disk_partitions()
            result = f"Information sur les partitions :\n {information_partition}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 1:
            fmt = "{:<20s} {:>8s} {:>8s} {:>8s} {:>8s}% {:8s} {:10s}"
            titre = fmt.format("Device", "Total", "Util.", "Libre", "% util", "Type", "Montage")
            for part in psutil.disk_partitions():
                usage = psutil.disk_usage(part.mountpoint)
                d_info = fmt.format(
                    part.device,
                    bytes2human(usage.total),
                    bytes2human(usage.used),
                    bytes2human(usage.free),
                    str(int(usage.percent)),
                    part.fstype,
                    part.mountpoint
                )
                d_info = titre + "\n" + d_info
            result = f"Information sur l'utilisation du disk(s) :\n {d_info}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 2:
            information_disk = psutil.disk_io_counters(perdisk=False)
            result = f"Information sur les disk(s) :\n {information_disk}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes memoire :


def fmt_ntuple(nt):
    r = []
    for name in nt._fields:
        valeur = getattr(nt, name)
        if name != 'percent':
            valeur = bytes2human(valeur)
        else:
            valeur = "{:5.2f}%".format(valeur)
        r.append("{:10s} : {:>7s}".format(name.capitalize(), valeur))
    return r


def memoire(item):
    try:
        if item == 0:
            mem_utiliser = psutil.virtual_memory().total - psutil.virtual_memory().available
            result = ("Mémoire ram utiliser : {}".format(
                int(mem_utiliser / 1024 / 1024)))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 1:
            mem_total = psutil.virtual_memory().total
            result = ("Mémoire ram total : {}".format(
                int(mem_total / 1024 / 1024)))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 2:
            mem_utilisation_pourcen = psutil.virtual_memory().percent
            result = ("Mémoire ram utiliser en % : {}".format(
                int(mem_utilisation_pourcen)))  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 3:
            mem = fmt_ntuple(psutil.virtual_memory())
            swp = fmt_ntuple(psutil.swap_memory())
            mx = max(len(mem), len(swp))
            mem += [" " * 20] * mx
            swp += [" " * 20] * mx
            result = "Memory".center(20) + ' | ' + "Swap".center(20) + ' |'
            for x in range(0, mx):
                result = result + "\n" + mem[x] + ' | ' + swp[
                    x] + ' |'  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes networks :


def networks(item):
    try:
        if item == 0:
            net0 = psutil.net_io_counters(pernic=True)
            fmt = "| {:>5s}| {:>11s}| {:>8s}| {:>14s}| {:>11s}| {:>20s}| {:>20s}|"
            titre = fmt.format("CARTE", "BIT ENVOYER", "BIT REÇU", "PACKET ENVOYER", "PACKET REÇU",
                               "PERTE DE PAQUETS / E", "PERTE DE PAQUETS / S")
            dd_info = titre
            for key in net0:
                part = psutil.net_io_counters(pernic=True)[key]
                d_info = fmt.format(
                    key,
                    bytes2human(part.bytes_sent),
                    bytes2human(part.bytes_recv),
                    str(part.packets_sent),
                    str(part.packets_recv),
                    str(part.errin),
                    str(part.errout)
                )
                dd_info = dd_info + "\n" + d_info
            result = f"Utilisation des carte reseaux :\n{dd_info}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 1:
            net1 = psutil.net_connections(kind='tcp')
            result = f"Résultat :\n {net1}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 2:
            net2 = psutil.net_if_addrs()
            result = f"Résultat :\n {net2}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 3:
            result = netstat()
            return result  # Renvoie le résultat pour l'envoyer
        if item == 4:
            net3 = psutil.net_if_stats()
            result = f"Résultat :\n {net3}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


def resolve(ip):
    try:
        data = socket.gethostbyaddr(ip)
        host = data[0]
    except:
        host = ''
    return host


def netstat():
    proc_name = {}

    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_name[p.info['pid']] = p.info['name']

    fmt = "{:25s}|{:25s}| {:20s}|{:15s}|{:s}"
    titre = fmt.format('Local', 'Distante', 'status', 'Process', 'Host')

    r = '=' * len(titre)
    titre = titre + "\n" + str(r)

    for c in psutil.net_connections(kind='inet4'):
        l = "%15s : %s" % (c.laddr[0], c.laddr[1])
        if c.raddr:
            r = "%15s : %s" % (c.raddr[0], c.raddr[1])
            host = resolve(c.raddr[0])
        else:
            r = ""
            host = ""
        s = c.status
        p = proc_name.get(c.pid, "")
        titre = titre + "\n" + fmt.format(l, r, s, p, host)     # Mise en Forme de la réponse à envoyer à l'utilisateur
    return titre


########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes pour les process :


def process(item):
    try:
        if item == 0:
            tous_process = pid_name()
            result = f"Liste de tous les processus ouverts :\n {tous_process}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 1:
            capteur_ventilo = psutil.sensors_fans()
            result = f"Information sur les ventilateurs:\n {capteur_ventilo}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 2:
            capteur_batterie = psutil.sensors_battery()
            result = f"Information sur la batterie:\n {capteur_batterie}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


def pid_name():
    fmt = "{:>4s}   {:>16s}          {:<2s}         {:>2s}"
    info_p = fmt.format("PID", "UTILISATEUR", "STATUE", "NOM")
    r = '=' * len(info_p)
    info_p = info_p + "\n" + str(r)
    for proc in psutil.process_iter():
        info = proc.as_dict(attrs=['pid', 'name', 'username', 'status'])
        info_p = info_p + "\n" + fmt.format(str(info.get("pid")), str(info.get("username")), str(info.get("status")), str(info.get("name")))
    return info_p


########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes pour les capteurs : Malheureusement non fonctionnel, car impossible à utiliser dans une VM


def capteur(item):
    try:
        if item == 0:
            capteur_temperature = psutil.sensors_temperatures()
            result = f"La température est de :\n {capteur_temperature}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 1:
            capteur_ventilo = psutil.sensors_fans()
            result = f"Information sur les ventilateurs:\n {capteur_ventilo}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 2:
            capteur_batterie = psutil.sensors_battery()
            result = f"Information sur la batterie:\n {capteur_batterie}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


########################################################################################################################
########################################################################################################################
# Fonction pour toutes les demandes sys_info :


def sys_info(item):
    try:
        if item == 0:
            sys_info_user = psutil.users()
            result = f"Les informations utilisateurs sont : \n {sys_info_user}"  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
        if item == 1:
            sys_date_h_machine = psutil.boot_time()
            result = "La machine est démarré depuis : "
            result = result + datetime.datetime.fromtimestamp(sys_date_h_machine).strftime(
                "%Y-%m-%d %H:%M:%S")  # Mise en Forme de la réponse à envoyer à l'utilisateur
            return result  # Renvoie le résultat pour l'envoyer
    except Exception as e:  # Montre l'erreur rencontrée par le script
        print(str(e))


########################################################################################################################
########################################################################################################################
# Fonction qui envoi tous les résultats au client :


def envoi(result):
    line = str.encode(result)               # Encode le résultat à envoyer au client
    os.write(fd_w, line)                    # Écriture du résultat dans le tube
    exit()                                  # Le fils quit le script il est ce suicide donc


########################################################################################################################
########################################################################################################################
# Partie serveur récup de la demande du client :

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
    # Définit "Menu" en utilisant la sous-chaîne de caractères de "x" allant de l'indice 0 à "NB"
    Menu = x[0:NB]
    
    try:
        Menu = int(Menu)
        Sous_menu = x[NB + 1:]
        Sous_menu = int(Sous_menu)
    except Exception as e:                      # Exception pour afficher quand le client se déconnecter
        print("Le client vien de quitter la session")
        exit()                                  # Quitte le script

    try:                                        # Debut gestion d'erreur pour le fils 
        child_pid = os.fork()                   # Création du Fils qui va effectuer la demande du client
    except Exception as e:                      # Renvoie dans "e" l'erreur rencontré par le fils
        print("Error in fork()")
        print(str(e))
        sys.exit(-1)

    if child_pid == 0:                          # seul le fils peut entrer dans ce IF
        print("Child:  PID =", os.getpid(),     # Affiche les infos du fils pour les tests et les débogages
              "  PPID =", os.getppid())
        if Menu == 0:                           # Choix du Menu
            # cpu
            result = cpu(Sous_menu)             # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
        if Menu == 1:                           # Choix du Menu
            # mem
            result = disk(Sous_menu)            # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
        if Menu == 2:                           # Choix du Menu
            # disk
            result = memoire(Sous_menu)         # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
        if Menu == 3:                           # Choix du Menu
            # netw
            result = networks(Sous_menu)        # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
        if Menu == 4:                           # Choix du Menu
            # pros
            result = process(Sous_menu)         # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
        if Menu == 5:                           # Choix du Menu
            # capteur   
            result = capteur(Sous_menu)         # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
        if Menu == 6:                           # Choix du Menu
            #  sysinfo
            result = sys_info(Sous_menu)        # Renvoie la demande à effectuer au menu choisie
            envoi(result)                       # Renvoie le résultat à la fonction envoi
    else:
        print("Parent: PID =", os.getpid(),     # Affiche les infos du père pour les tests et les débogages
              "  PPID =", os.getppid(),
              "  Child =", child_pid)
        os.wait()

