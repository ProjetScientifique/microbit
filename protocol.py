import radio

class RadioProtocol:
    def __init__(self, address, shiftPattern, queue = []):
        self.addr = address
        self.shiftPattern = shiftPattern
        self.queue = queue

    def sendHelper(self, cliAdd, msg) :
        idMsg = msg.split('"idMsg": ')[1].split(",")[0]
        print(idMsg)
        radio.send_bytes("" + str(self.addr) + "|||" + str(len(msg)) + "|||" + str(cliAdd) + "|||" + self.encrypt(msg) + "|||" + str(idMsg) + "|||" + str(self.calculateChecksum(msg)))

    def sendByRadio(self, message, addrDest):
        self.sendHelper(addrDest, str(message))

    def receiveByRadio(self):
        incMessage = radio.receive_bytes()
        if incMessage != None :
            tabRes = incMessage.format(1).split("|||")
            if len(tabRes) != 6 :
                return -1
            data = dict()
            data['addrInc'] = tabRes[0]
            data['lenMess'] = tabRes[1]
            data['addrDest'] = tabRes[2]
            data['receivedCheckSum'] = tabRes[5]
            if self.addr == int(data['addrDest']):
                data['message'] = self.decrypt(tabRes[3])
                data['idMsg'] = tabRes[4]
                if self.verifyCheckSum(data['receivedCheckSum'], self.calculateChecksum(data['message'])):
                    if data['message'] != "ACK" and data['message'] != "NACK" :
                        self.sendHelper(data['addrInc'], "ACK")
                    return data['message']
                else :
                    self.sendHelper(data['addrInc'], "NACK")
                    return -1
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

