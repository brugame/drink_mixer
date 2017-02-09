import RPi.GPIO as GPIO
import time
import threading

#define drink list
drink_list={"Drink 1": [0,1,2], "Drink 2": [1,3,0], "Drink 3": [1,1,1]}

#define all pins
liquid1=2
liquid2=3
liquid3=4
button1=17
button2=27
button3=22

#Motor control pins
enable_pin = 21
coil_A_1_pin = 20
coil_A_2_pin = 16
coil_B_1_pin = 26
coil_B_2_pin = 19

#LCD control pins
#lcd_rs        = 27  
#lcd_en        = 22
#lcd_d4        = 25
#lcd_d5        = 24
#lcd_d6        = 23
#lcd_d7        = 18

#Specify 20x4 LCD
lcd_columns = 20
lcd_rows    = 4

#Define GPIO mode and init pins

GPIO.setmode(GPIO.BCM)

GPIO.setup(liquid1, GPIO.OUT)
GPIO.setup(liquid2, GPIO.OUT)
GPIO.setup(liquid2, GPIO.OUT)

#set pulldown resistors for buttons to have default value of true
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

#Init LCD display 
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

#define motor control functions, move this to a library later
def forward(delay, steps):
	for i in range(0, steps):
		setStep(1, 0, 1, 0)
		time.sleep(delay)
		setStep(0, 1, 1, 0)
		time.sleep(delay)
		setStep(0, 1, 0, 1)
		time.sleep(delay)
		setStep(1, 0, 0, 1)
		time.sleep(delay)
    
def backwards(delay, steps):  
	for i in range(0, steps):
		setStep(1, 0, 0, 1)
		time.sleep(delay)
		setStep(0, 1, 0, 1)
		time.sleep(delay)
		setStep(0, 1, 1, 0)
		time.sleep(delay)
		setStep(1, 0, 1, 0)
		time.sleep(delay)
    
def setStep(w1, w2, w3, w4):
	GPIO.output(coil_A_1_pin, w1)
	GPIO.output(coil_A_2_pin, w2)
	GPIO.output(coil_B_1_pin, w3)
	GPIO.output(coil_B_2_pin, w4)
    
def dispense(delay_value, drinknumber):
	if delay_value>0:
		GPIO.output(drinknumber,1)
		time.sleep(delay_value*2.0)
		GPIO.output(drinknumber,0)
        
#define release drink function
def releaseDrink(Drink_List, drinkName):
	drink_found=0
	threads=[]
	for name in Drink_List:
		if name==drinkName:
		    drink_found=1
			lcd.clear()
			lcd.message('Dispensing %s', drinkName)
			liquids=Drink_List.get(drinkName)
			for i in range(len(liquids)-1):
				t=threading.Thread(target=dispense, args=(liquids[i],i+1))
				threads.append(t)
				t.start()
			for t in threads:
				t.join()
	if drink_found != 1:
    lcd.clear()
    lcd.message('No Valid Drink Found')
    
#Show start message, go into infinite loop
lcd.clear()
lcd.message('Drink Miver V1.0')

while True:
	if GPIO.input(button1) == True:
		releaseDrink(drink_list,"Drink 1")
	else if GPIO.input(button2) == True:
		releaseDrink(drink_list,"Drink 2")
	else if GPIO.input(button3) == True:
		releaseDrink(drink_list,"Drink 3")
	else:
		lcd.clear()
		lcd.message('Waiting for command')
	time.sleep(1.0)
