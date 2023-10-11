import sqlite3
import time

# Chemin vers la base de données
dbname = '/var/www/html/soft_project/Client/BD/farm_water.db'

# Fonction pour enregistrer le statut de la pompe dans la base de données
def log_pump_status(pump_status):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("INSERT INTO pompe_table (time_of_launching_pump, pump_status) VALUES (datetime('now'), ?)", (pump_status,))
    conn.commit()
    conn.close()

# Fonction pour récupérer la valeur du capteur de niveau d'eau depuis le fichier
def get_sensor_value():
    # Chemin vers le fichier du capteur de niveau d'eau
    sensor_file = '/path/to/sensor_file_emulator.txt'

    # Lecture de la valeur du capteur à partir du fichier
    with open('/var/www/html/soft_project/Serveur/Python/sensor_file_emulator.txt', 'r') as file:
        sensor_value = float(file.read())

    return sensor_value

HIGH_LEVEL_OF_WATER = 90.0
LOW_LEVEL_OF_WATER = 87.0

# Activer la pompe (pump_value = ON)
my_functions.turn_pump_on()

# Enregistrer l'heure de lancement de la pompe dans la base de données
log_pump_status(1)

while get_sensor_value() <= HIGH_LEVEL_OF_WATER:
    # Code pour incrémenter le niveau d'eau pendant que la pompe est en marche
    # Remplacez cette partie avec votre propre logique pour simuler l'incrémentation du niveau d'eau en temps réel
    print("La pompe est en marche... pompe = ON")
    time.sleep(2)

print("Le niveau d'eau est supérieur au niveau maximal du réservoir")

# Allumer la LED de niveau élevé (high_level_led = ON)
my_functions.turn_high_level_led_on()

# Éteindre la pompe (pump_value = OFF)
my_functions.turn_pump_off()
print("Pompe éteinte... pompe = OFF")

# Enregistrer le statut de la pompe dans la base de données
log_pump_status(0)



