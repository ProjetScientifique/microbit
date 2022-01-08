import radio

class RadioProtocol:
    def __init__(self, address, shiftPattern, queue = []): 
        self.addr = address
        self.shiftPattern = shiftPattern        

    ## Send data by radio to a microbit with the given address
    def sendByRadio(self, addrDest, message):
        radio.send_bytes("" + str(self.addr) + "|||" + str(len(message)) + "|||" + str(addrDest) + "|||" + self.encrypt(message) + "|||" + str(self.calculateChecksum(message)))

    ## Receive data by Radio
    def receiveByRadio(self):
        incMessage = radio.receive_bytes() # Get bytes
        if incMessage != None :
            tabRes = incMessage.format(1).split("|||") # Split according to the pattern we designed for our protocol
            if len(tabRes) != 5 : # Check if the split actually returned an array the right len 
                return -1
            data = dict() # Store data to a dictionnary
            data['addrInc'] = tabRes[0]
            data['lenMess'] = tabRes[1]
            data['addrDest'] = tabRes[2]
            data['receivedCheckSum'] = tabRes[4]
            if self.addr == int(data['addrDest']): # If msg was destined to us
                data['message'] = self.decrypt(tabRes[3])
                if self.verifyCheckSum(data['receivedCheckSum'], self.calculateChecksum(data['message'])): # If checksum is ok
                    if data['message'] != "ACK" and data['message'] != "NACK" : # Makes sure that the message isn't ACK or NACK
                        self.sendByRadio(data['addrInc'], "ACK")
                    return data['message']
                else :
                    self.sendByRadio(data['addrInc'], "NACK")
                    return -1
        return 0

    ## Used to encrypt data by shifting letters according to the shiftPattern chosen in the __init__ function
    def encrypt(self, msg):
        res = ""
        for i in range(len(msg)):
            res += chr(ord(msg[i])+self.shiftPattern)
        return res

    ## Used to decrypt data by shifting letters according to the shiftPattern chosen in the __init__ function
    def decrypt(self, msg):
        res = ""
        for i in range(len(msg)):
            res += chr(ord(msg[i])-self.shiftPattern)
        return res

    # Calculates checksum for a given message
    def calculateChecksum(self, message):
        nleft = len(message)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(message[pos]) * 256 + (ord(message[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            sum = sum + ord(message[pos]) * 256

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)

        return sum
    
    # Verify a given checksum for a given message
    def verifyCheckSum(self, checkSum, receivedCheckSum):
        if int(checkSum) == receivedCheckSum:
            return True
        else:
            return False

