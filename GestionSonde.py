# Initialisation de la variable permettant de trouver le fichier ou est stocke la temperature via la sonde DALLAS
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

TableauBuffer = [] # Creation du tableau qui sert de buffer si internert est off

# Fonction pour lire le contenu du fichier des temperatures
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Fonction pour lire le contenu et l'analyser pour trouver la valeur de la temperature
def read_temp():
    lines = read_temp_raw()
    # Si le fichier ne contient paqs le mot YES, c'est qu'il y a un probleme, on retourne alors -200
    if lines[0].strip()[-3:] != 'YES':
        return -200
    equals_pos = lines[1].find('t=')  # On regarde la position du mot t= dans la seconde ligne du fichier
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 100.0
        return int(temp_c)
