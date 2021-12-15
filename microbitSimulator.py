from microbit import *
import radio
import protocol

# MAINTENANT FAUT ADD LE FAAIT QUE CHAQUE FDP DOIT EN PERMANANCE RECEIVE BY RADIO AFIN DE CHECK QUE LE MSG ENVOYE A BIEN ETE RECU !!!!!


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
while True: # Ptet print la queue pour être sur que is ok ?
    msgInfo = radioProtocol.receiveByRadio()
    if msgInfo != None and msgInfo != 0 :
        print(msgInfo)
    msgUart = uart.read()
    if msgUart != None :
        radioProtocol.sendByRadio(str(msgUart), 1)
