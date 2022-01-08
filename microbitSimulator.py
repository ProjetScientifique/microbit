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
        msgToSend = str(uart.read(), 'utf-8')
        dataSplit = msgToSend.split("|||")
        if len(dataSplit) != 1 :
            if str(radioProtocol.calculateChecksum(dataSplit[0])) == dataSplit[1] :
                radioProtocol.sendByRadio(str(dataSplit[0],'utf-8'), 1)
            else :
                uart.write("NACK\n")
        else :
            uart.write("NACK\n")
