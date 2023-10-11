/*
 * c_module_for_python.c
 *
 *      Author: Maroua Radouan
 */

 #include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#include "io.h"		

S_GPIO_LINE s_line_pump, s_line_high_level_led, s_line_low_level_led;

void init_all_used_GPIO(void){

	load_gpio_line(&s_line_pump, PIN17 , OUT) ;
	load_gpio_line(&s_line_high_level_led, PIN18 , OUT) ;
	load_gpio_line(&s_line_low_level_led, PIN22 , OUT) ;
	return;
}

void turn_pump_on(void){
	
	set_gpio_line(&s_line_pump,1);
}

void turn_pump_off(void){
	set_gpio_line(&s_line_pump,0);
}

//high_level_led

void turn_high_level_led_on(void){
	set_gpio_line(&s_line_high_level_led,1);
}

void turn_high_level_led_off(void){
	set_gpio_line(&s_line_high_level_led,0);
}

//low_level_led

void turn_low_level_led_on(void){
	set_gpio_line(&s_line_low_level_led,1);
}

void turn_low_level_led_off(void){
	set_gpio_line(&s_line_low_level_led,0);
}
	

