# -*- coding: utf-8 -*-
import smbus
import time
# for RPI version 1, use "bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

val = 1
while True:
    var = 1
    if not var:
        continue
    try:
        writeNumber(var)
        print "RPI: Hi Arduino, I sent you ", var
        # sleep one second
        time.sleep(0.1)
        
        number = readNumber()
        print "Arduino: Hey RPI, I received a digit ", number
        print
    except IOError:
        print "skipping"
        
        val = (val + 1) % 8
