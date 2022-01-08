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
        ## Receive message by radio
        msgReceived = radioProtocol.receiveByRadio()
        if msgReceived != 0 and msgReceived != None : # Make sure the message isn't empty, 0 is the value return when the receiveByRadio function receives a None object
            uart.write(msgReceived + "\n")
