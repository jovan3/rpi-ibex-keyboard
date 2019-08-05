import RPi.GPIO as GPIO
import time
import smbus
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bus = smbus.SMBus(1)
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

def i2c_interrupt(channel):
    try:
        writeNumber(1)
        print "RPI: Hi Arduino, I sent you 1"
        # sleep one second
        time.sleep(0.1)

        number = readNumber()
        print "Arduino: Hey RPI, I received a digit ", number
        print
    except IOError:
        print "skipping"

        
GPIO.add_event_detect(11, GPIO.FALLING, callback=i2c_interrupt, bouncetime=10)

try: 
    while True:
	time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
        
GPIO.cleanup()           # clean up GPIO on normal exit
