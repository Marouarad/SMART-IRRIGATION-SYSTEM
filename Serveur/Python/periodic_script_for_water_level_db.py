#!/usr/bin/env python

import sqlite3
import random
import time

# Connexion à la base de données
conn = sqlite3.connect('/var/www/html/soft_project/Client/BD/farm_water.db')
c = conn.cursor()

while True:
    # Génération d'une valeur aléatoire pour le niveau d'eau
    water_level = random.uniform(0, 100)

    # Insertion de la valeur dans la base de données
    c.execute("INSERT INTO water_level (timestamp, level) VALUES (?, ?)", (int(time.time()), water_level))
    conn.commit()

    # Affichage des données
    c.execute("SELECT * FROM water_level ORDER BY timestamp DESC LIMIT 1")
    row = c.fetchone()
    print("Timestamp: ", row[0])
    print("Water Level: ", row[1])

    # Attente de 1 seconde avant la prochaine insertion
    time.sleep(1)

# Fermeture de la connexion à la base de données
conn.close()


