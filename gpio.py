import RPi.GPIO as GPIO
import time
import smbus
import time
import input

GPIO_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bus = smbus.SMBus(1)
address = 0x04

keyboard_uinput = input.Input()

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

def i2c_interrupt(channel):
    try:
        number = readNumber()
        print("Arduino: Hey RPI, I received a digit ", number)
        keyboard_uinput.do_i2c_code(number)
        print()
    except IOError:
        print("skipping")

        
GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=i2c_interrupt, bouncetime=10)

try: 
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
        
GPIO.cleanup()           # clean up GPIO on normal exit
