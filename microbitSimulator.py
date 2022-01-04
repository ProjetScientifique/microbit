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
radio.config(group = 2, length = 251, queue = 12)
radio.on()

'''
 * main program
'''
while True:
    msgInfo = radioProtocol.receiveByRadio()
    msgUart = uart.read()
    if msgInfo != None and msgInfo != 0 :
        print(msgInfo)
        #uart.write("b'" + msgInfo + "'")  # apparament ça c'est bloquant :)d:)d:d)za:d)
    if msgUart != None :
        radioProtocol.sendByRadio(str(msgUart), 1)