/*
 * io.h
 *
 *      Author: Maroua Radouan
 */
 
 #ifndef IO_H_
#define IO_H_


#define PIN17 "17"
#define PIN18 "18"   
#define PIN22 "22"   
#define PIN23 "23"   
#define PIN24 "24"   
#define PIN25 "25"   
#define PIN26 "26" 
#define PIN27 "27"       

#define LOW  0
#define HIGH 1
#define IN   1
#define OUT  0

struct S_GPIO_LINE {
    char id_number[4];
    int direction;
    int value;
};
typedef struct S_GPIO_LINE S_GPIO_LINE;


int load_gpio_line(S_GPIO_LINE *ps_line, char id_number[4], int i_direction);
int set_gpio_direction(S_GPIO_LINE *ps_line, int i_direction);
int set_gpio_line(S_GPIO_LINE *ps_line, int value);
int get_gpio_line(S_GPIO_LINE *ps_line);

#endif /*IO_H_*/
