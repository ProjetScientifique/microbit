from microbit import *
import radio
import protocol


'''
 * variable for script
'''
radioProtocol = protocol.RadioProtocol(2,3)


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
    #msgInfo = radioProtocol.receiveByRadio()
    msgUart = uart.read()
    if msgUart != None :
        print("ok: " +  str(msgUart))
        #uart.write(radioProtocol.sendByRadio(str(msgUart), 1))
