#!/usr/bin/env python

import sqlite3

# Chemin vers la base de données
dbname = '/var/www/html/soft_project/Client/BD/farm_water.db'

# Chemin vers le fichier émulant le capteur
sensor_file = '/var/www/html/soft_project/Serveur/Python/sensor_file_emulator.txt'

# Fonction pour obtenir le niveau d'eau
# Renvoie None en cas d'erreur ou la valeur du niveau d'eau sous forme de chaîne
def get_water_level():
    with open(sensor_file, 'r') as file:
        water_level = file.read().strip()
    return water_level

# Fonction pour enregistrer le niveau d'eau dans la base de données
def log_water_level(water_level):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("INSERT INTO water_level_table values(datetime('now'), (?))", (water_level,))
    conn.commit()
    conn.close()

# Fonction pour afficher le contenu de la base de données
def display_data():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT * FROM water_level_table WHERE rowid = (SELECT MAX(rowid) FROM water_level_table)")
    rows = c.fetchall()
    for row in rows:
        print("{} | {}".format(row[0], row[1]))
    conn.close()

# Fonction principale
def main():
    water_level = get_water_level()
    if water_level is not None:
        print("Water level = {}".format(water_level))
        log_water_level(water_level)
        display_data()

if __name__ == "__main__":
    main()


