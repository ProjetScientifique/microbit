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
radio.config(group = 2, length = 251)
radio.on()

'''
 * main program
'''
while True:
        newMsg = radioProtocol.receiveByRadio()
        if newMsg != 0 :
            print(newMsg)
