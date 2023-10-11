#################################################
#				used libararies					#
#################################################

import manipulating_sensor_file
import asyncio
import script_pump_for_db

#################################################
#					constants:					#
#################################################
HIGH_LEVEL_OF_WATER = 90.0
LOW_LEVEL_OF_WATER = 87.0

#################################################
#					variables					#
#################################################

#################################################
#					modules:					#
#################################################

#################################################################################################
# import a shared library wrotten in C that contains all functions for writing in GPIO Pins 	#
# we used 3 pins : 													 							#
#		* pin pour marche/arret de la pompe 											 		#
#		* pin pour indiquer que le niveau d'eau dans le reservoire atteidre le niveau max 		#
#		* pin pour indiquer que le niveau d'eau dans le reservoire atteidre le niveau min 		#
#################################################################################################

from ctypes import *

# chemin pour shared library qu'on a cree 
so_file = "/var/www/html/Serveur/Drivers/my_functions.so"

# make the functions as a python module 
my_functions = CDLL(so_file)

# fonction pour initialisation des 3 pins 
my_functions.init_all_used_GPIO()

##################################################################################################
# emulation du capteur pour la diminution du quantitee d'eau									 #
##################################################################################################
async def level_decrease():
	while True :
		manipulating_sensor_file.init_sensor()
		manipulating_sensor_file.set_sensor_value()
		await asyncio.sleep(3)


##################################################################################################
# emulation du capteur lors du remplissage du reservoire 										 #
##################################################################################################
async def level_increase():
	while True :
		if (manipulating_sensor_file.get_sensor_value() <= HIGH_LEVEL_OF_WATER) and (manipulating_sensor_file.get_sensor_value() >= LOW_LEVEL_OF_WATER) :
			print("niveau d'eau est au niveau moyen du r  servoir")
			#high_level_led = OFF
			my_functions.turn_high_level_led_off()
			#low_level_led = OFF
			my_functions.turn_low_level_led_off()
		elif manipulating_sensor_file.get_sensor_value() <= LOW_LEVEL_OF_WATER :
			#low_level_led = ON
			print("niveau d'eau est inferieur au niveau minimal du r  servoir")
			my_functions.turn_low_level_led_on()
			#pump_value =ON
			my_functions.turn_pump_on()
			script_pump_for_db.log_time_of_launching_pump()
			
			while manipulating_sensor_file.get_sensor_value() <= HIGH_LEVEL_OF_WATER :
				if manipulating_sensor_file.get_sensor_value() >= LOW_LEVEL_OF_WATER :
					#low_level_led = OFF
					my_functions.turn_low_level_led_off()
				manipulating_sensor_file.increment_level_while_pump_turned_on() 
				print("la pompe pompe maintenant ..., pompe = ON")
				await asyncio.sleep(4)

			print("niveau d'eau est superieur au niveau maximal du r  servoir")
			#high_level_led = ON
			my_functions.turn_high_level_led_on()
			#pump_value = OFF
			my_functions.turn_pump_off()
			print("pompe = OFF")

		await asyncio.sleep(2)
		
		
##################################################################################################
# synchronization entre l'augmentation et la diminution de l'eau dans le reservoir				 #
################################################################################################## 
async def main_function() :
	manipulating_sensor_file.init_sensor()
	await asyncio.gather(
		level_decrease(),
		level_increase()
	)
		
asyncio.run(main_function())
