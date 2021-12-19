import radio

MESSAGE_ERROR = "CHECKSUM ERROR"
MESSAGE_SUCCESS = "DATA RECEIVED"

class RadioProtocol:
    def __init__(self, address, shiftPattern, queue = []):
        self.addr = address
        self.shiftPattern = shiftPattern
        self.queue = queue

    def sendHelper(self, cliAdd, msg) :
        radio.send_bytes("" + str(self.addr) + "|||" + str(len(msg)) + "|||" + str(cliAdd) + "|||" + self.encrypt(msg) + "|||" + str(self.calculateChecksum(msg)))

    def sendByRadio(self, message, addrDest):
        messageToSend = ""
        i = 0
        arr = str(message).replace("b'", "")[:-1].split("\\n")
        while i < len(arr) :
            if len(messageToSend + arr[i]) < 243 :
                messageToSend += arr[i]
                i = i + 1
            else : 
                print(messageToSend)
                self.sendHelper(addrDest, messageToSend)
                messageToSend = ""
        if messageToSend != "" :
            print(messageToSend)
            self.sendHelper(addrDest, messageToSend)

    def receiveByRadio(self):# RADIO RECEIVE BYTES ICI !
        incMessage = radio.receive_bytes()
        if incMessage != None :
            print(incMessage)
            tabRes = incMessage.format(1).split("|||")
            if len(tabRes) != 5 :
                return -1
            data = dict()
            data['addrInc'] = tabRes[0]
            data['lenMess'] = tabRes[1]
            data['addrDest'] = tabRes[2]
            data['receivedCheckSum'] = tabRes[4]
            if self.addr == int(data['addrDest']):
                data['message'] = self.decrypt(tabRes[3])
                if self.verifyCheckSum(data['receivedCheckSum'], self.calculateChecksum(data['message'])):
                    if data['message'] == MESSAGE_SUCCESS :
                        print("ACK")
                        return 1
                    elif data['message'] == MESSAGE_ERROR :
                        print("NACK")
                        return 2
                    else :
                        self.sendHelper(data['addrInc'], MESSAGE_SUCCESS)
                        return data['message']
                else :
                    self.sendHelper(data['addrInc'], MESSAGE_ERROR)
                    return 3
        return 0

    def encrypt(self, msg):
        res = ""
        for i in range(len(msg)):
            res += chr(ord(msg[i])+self.shiftPattern)
        return res

    def decrypt(self, msg):
        res = ""
        for i in range(len(msg)):
            res += chr(ord(msg[i])-self.shiftPattern)
        return res

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
    
    def verifyCheckSum(self, checkSum, receivedCheckSum):
        if int(checkSum) == receivedCheckSum:
            return True
        else:
            return False

