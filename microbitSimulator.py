from microbit import *
import radio
import protocol


'''
 * variable for script
'''
radioProtocol = protocol.RadioProtocol(2,3)
msgReceived = ""

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
    ## Checking for potential message sent by Radio, and sending it to the Gateway
    msgInfo = radioProtocol.receiveByRadio()
    if msgInfo != None and msgInfo != 0 :
        uart.write(msgInfo + "\n")
    ## Getting data sent by the Gateway
    if uart.any():
        msgToSend = uart.read()
        radioProtocol.sendByRadio(str(msgToSend,'utf-8'), 1)
    '''
    if uart.any():
        msgToSend = str(uart.read(),'utf-8')
        verif = False
        while verif == False :
            if uart.any() :
                msg = str(uart.read(),'utf-8')
                if msg == "ACK":
                    radioProtocol.sendByRadio(str(msgToSend,'utf-8'), 1)
                    verif = True
                else :
                    uart.write(msg + "\n")
    '''