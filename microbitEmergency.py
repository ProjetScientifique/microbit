# Ecrit ton programme ici ;-)
from microbit import *
import protocol
import radio

'''
 * variable for script
'''
radioProtocol = protocol.RadioProtocol(1,3)

'''
 * init comm
'''
uart.init(115200)
radio.config(group = 2, length = 251, queue = 5)
radio.on()

'''
 * main program
'''
while True:
        msgReceived = radioProtocol.receiveByRadio()
        if msgReceived != 0 and msgReceived != None :
            uart.write(msgReceived + "\n")
