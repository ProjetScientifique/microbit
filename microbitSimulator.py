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
    msgInfo = radioProtocol.receiveByRadio()
    if msgInfo != None and msgInfo != 0 and msgInfo != -1 :
        uart.write(msgInfo)
    msgUart = uart.read()
    if msgUart != None :
        print("ok: " +  str(msgUart))
        radioProtocol.sendByRadio(str(msgUart), 1)
