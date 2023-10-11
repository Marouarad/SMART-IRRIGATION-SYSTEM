#!/usr/bin/env python
#################################################
#                 used libraries                #
#################################################
import sys
import sqlite3

# Insert the path to the necessary modules
sys.path.insert(1, '/var/www/html/Serveur/Python')

import script_pump_for_db

#################################################
#               Constants                       #
#################################################
HIGH_LEVEL_OF_WATER = 90.0
LOW_LEVEL_OF_WATER = 87.0

#################################################
#           Database path
#################################################
dbname = '/var/www/html/soft_project/Client/BD/farm_water.db'

#################################################
#           Function to update pump status in the database
#################################################
def update_pump_status(status):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("UPDATE pompe_table SET pump_status = ? WHERE time_of_launching_pump = (SELECT MAX(time_of_launching_pump) FROM pompe_table)", (status,))
    conn.commit()
    conn.close()

#################################################
#           Function to get pump status from the database
#################################################
def get_pump_status():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT pump_status FROM pompe_table WHERE time_of_launching_pump = (SELECT MAX(time_of_launching_pump) FROM pompe_table)")
    status = c.fetchone()[0]
    conn.close()
    return status

###############################################
#           Main code
###############################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'start_pumping':
            # Check if pump is already running
            status = get_pump_status()
            
            if status == 0:
                update_pump_status(1)  # Update pump status to active
                print("La pompe est activée.")
            else:
                print("La pompe est déjà en marche.")
        
        if command == 'stop_pumping':
            # Check if pump is already stopped
            status = get_pump_status()
            
            if status == 1:
                update_pump_status(0)  # Update pump status to inactive
                print("La pompe est désactivée.")
            else:
                print("La pompe est déjà arrêtée.")
    
    # Check water level
    with open('/var/www/html/soft_project/Serveur/Python/sensor_file_emulator.txt', 'r') as file:
        water_level = float(file.read())
    
    if water_level > HIGH_LEVEL_OF_WATER:
        # Stop pumping
        update_pump_status(0)
        print("La pompe est désactivée car le niveau d'eau est trop élevé.")

