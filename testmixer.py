import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import speech_recognition as sr
from multiprocessing import Process


#define drink list
drink_list={"pina colada": [2,0,1], "whiskey": [2,3,0], "vodka": [2,2,2]}

#define all pins
liquid1=2
liquid2=3
liquid3=4
button1=10
button2=9
button3=11

#Motor control pins
enable_pin = 21
coil_A_1_pin = 20
coil_A_2_pin = 16
coil_B_1_pin = 26
coil_B_2_pin = 19

#LCD control pins
lcd_rs        = 17  
lcd_en        = 27
lcd_d4        = 22
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18

#Specify 20x4 LCD
lcd_columns = 20
lcd_rows    = 4

#Define GPIO mode and init pins

GPIO.setmode(GPIO.BCM)

GPIO.setup(liquid1, GPIO.OUT)
GPIO.setup(liquid2, GPIO.OUT)
GPIO.setup(liquid3, GPIO.OUT)
GPIO.output(liquid1,0)
GPIO.output(liquid2,0)
GPIO.output(liquid3,0)

#set pulldown resistors for buttons to have default value of true
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

#gets string from what was said
def getOrder():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        lcd.clear()
        lcd.message('Place order')
        audio = r.record(source,4)

    try:
        order = r.recognize_google(audio)
        lcd.clear()
        lcd.message(order)
        time.sleep(3)
        return order
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return 'error1'
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return 'error2'

#checks if any 3 characters in the order matches 3 letters from the drink names
#returns the drink name if found
#returns 'not found' if no drink is found
def getName(Drink_List, drinkOrder):
    drinkOrder=drinkOrder.lower()
    for name in Drink_List:
        name=name.lower()
        for i in range (0,len(drinkOrder)-2):
            for j in range (0,len(name)-2):
                if (name[j]==drinkOrder[i]):
                    if (name[j+1]==drinkOrder[i+1]):
                        if (name[j+2]==drinkOrder[i+2]):
                            return name
    return ''
        
        
#define release drink function
def releaseDrink(Drink_List, drinkName):
    liquidnumbers=[liquid1,liquid2,liquid3]
    drink_found=0
    for name in Drink_List:
        if name==drinkName:
            liquids=Drink_List.get(drinkName)
            drink_found=1
            lcd.clear()
            lcd.message("Dispensing " + drinkName)
            liquids, liquidnumbers = zip(*sorted(zip(liquids, liquidnumbers)))
            for i in range(0,len(liquids)):
                if liquids[i] > 0:
                    GPIO.output(liquidnumbers[i],1)
            for j in range(0,len(liquids)):
                if j==0:
                    time.sleep(liquids[j]*0.5)
                    GPIO.output(liquidnumbers[j],0)
                else:
                    time.sleep((liquids[j]-liquids[j-1]) * 0.5)
                    GPIO.output(liquidnumbers[j],0)
    if drink_found != 1:
        lcd.clear()
        lcd.message('No drink found')


    
#Show start message, go into infinite loop
lcd.clear()
lcd.message('Drink Mixer V1.0')
time.sleep(2.0)

while True:
    lcd.clear()
    lcd.message("waiting for command")
    if GPIO.input(button1) == True:
        drinkOrder=getOrder();
        if drinkOrder == 'error1':
            lcd.message('Could not understand audio')
        elif drinkOrder == 'error2':
            lcd.message('Could not connect to Google Speech Recognition')
        else:
            drinkName=getName(drink_list,drinkOrder)
            releaseDrink(drink_list,drinkName)
    elif GPIO.input(button2) == True:
        drinkOrder=getOrder();
        releaseDrink(drink_list,drinkOrder)
    elif GPIO.input(button3) == True:
        drinkOrder=getOrder();
        releaseDrink(drink_list,drinkOrder)
    time.sleep(1.0)
