from microbit import *
import radio

def getFromUART()->(None or str):
    """
    Recupere les commandes souhaitées par le Téléphone.
    Il existe une fonctionnalité de Debug avec les deux boutons
    """
    recep = uart.read()
    if recep:
        return str(recep,'utf-8')
    #Man pr debug.
    #if button_a.was_pressed():
    #    return "TL"
    #if button_b.was_pressed():
    #    return "LT"
    return 0   

class Secu:
    """
    Class de sécurité, comprend toutes les fonctionnalités liées à la Sécu entre les microbits.       
    Securité. vraiment très sur!
    Algo de césar remodifié car on est vraiement très chaud  ! 
    """
    def crypt(self,message:str,key:int=10)->str:
        """
        Passe un message clair, le return en message crypté 
        Utilisation d'un césar modifié.
        """
        cryptedMessage = ""
        for lettre in message:
            key+=1 #pour chaque itération on décale la key de 1 
            cryptedMessage += chr(ord(lettre)+key)
        return cryptedMessage

    def decrypt(self,cryptedMessage:str,key:int=10)->str:
        """
        Passe un message crypté et une clef, le return en message clair. 
        Utilisation d'un césar modifié.
        """
        clearMessage = ""
        for lettre in cryptedMessage:
            key+=1 #pour chaque itération on décale la key de 1 
            clearMessage += chr(ord(lettre)-key)
        return clearMessage
        
    def checksum(self,message:str)->str:
        """
        fonction de checksum entre les deux microbits.
        Nous permet de verifier l'intégrité du message.
        #Reste très basic car si un octet du message est incrémenté et un second décrémenté alors l'intégrité sera vue comme juste.
        """
        checksum = 0
        for letter in message:
            checksum += ord(letter)
        return str(checksum)
    
    """
    import hashlib ne fonctionne pas :/
    def checksum(self,message):
        return hashlib.md5(message.encode()).hexdigest()
    """
    
    
class ProtocoleRadio:
    """
    Classe protocoleRadio.
	Comprend toutes les fonctionnalités pour envoyer et recevoir des messages 
    """
    def __init__(self,identifiant)->None:
        self.moi = identifiant #Mon identifiant sur le protocole.
    
    def get_message(self)->str and str:
        """
        Fonctionnalité pour recevoir les messages sur le protocole qui me sont destinés.
        """
        recep = radio.receive()
        if recep:
            message_recup = Secu().decrypt(recep).split("|")
            if message_recup[0] == self.moi:
                checksum = message_recup[-1]
                if checksum = message_recup[3]:
                    #Pas de confirmation
                    message_recup.pop()
                    message = '|'.join(message_recup)
                    if Secu().checksum(message) == checksum:
                        #le message s'addresse a moi.
                        return message_recup[1],message_recup[2]#1 source,message
                else:
                    message_recup.pop()
                    message = '|'.join(message_recup)
                    if Secu().checksum(message) == checksum:
                        if message_recup[3] == "confirmation":
                            send_message(message_recup[1],"confirmation",confirmation=False)
                        #le message s'addresse a moi.
                        return message_recup[1],message_recup[2]#1 source,message
        return 0,0

    def send_message(self,dest:str,msg:str,confirmation:bool=False)->bool:
        """
        Envoie un message crypté sous le format 
        "dest|source|message|checksum"
        ou 
        "dest|source|message|confirmation|checksum"
        
        PAr défaut la confirmation de reception de message est a False :
        send_message(destinatare,"message",confirmation=True)
            return True si on a la confirmation que le message à été pris en compte par la microbit.
            
        si confirmation = False 
            return True dès l'envoi du message.
        """
        to_send_informations = dest+"|"+self.moi+"|"+msg
        if confirmation:
            to_send_informations += "|confirmation" 
            
        to_send = to_send_informations+"|"+Secu().hash(to_send_informations)        
        radio.send(Secu().crypt(to_send))
        if confirmation:
            if confirmationReception(dest):
                return True
            else:
                return False
        return True
            
    def confirmationReception(destinataire:str)->bool
        reponse = False
        iteration = 0
        while not reponse:
            source,message = get_message()
            if source == destinataire and message == "confirmation":
                return True#reponse = True
            iteration += 1
            sleep(100)
            if iteration > 50
                return False
                

"""CODE PRINCIPAL POUR LE RECEIVER CONNECTE A LA PASSERELLE"""
if __name__ == "__main__":
    """DECLARATION DES IDENTIFIANT DES DEUX MACHINES."""
    IDENTIFIANT_EMETTEUR  = "ceec24f000b8209f27dd5560723beec5ee76679024ad4d32fc526e6539315f53"[:10]
    IDENTIFIANT_RECEPTEUR = "a16d113aedf022c5a016b44f7425ad643869a4581d63b13382c90f9117d8af87"[:10]
    
    #init radio
    radio.config(channel=24)#les deux channels doivent être identique entre les deux microbits.
    radio.on()
    uart.init(115200)
    
    
    #init protocoleRadio
    MON_IDENTIFIANT = #a changer
    PRadio = ProtocoleRadio(MON_IDENTIFIANT)
    while True:
        """
        Main Boucle
        """
        message_a_transmettre = getFromUART()#commande recu par le téléphone.
        if message_a_transmettre:
            PRadio.send_message(message_a_transmettre)
            ###
            ###ATTENTE DE LA CONFIRMATION DE RECEPTION.
            ###
            sleep(500)
            uart.write(bytes(message,'utf-8'))#envoi a la raspberry la réponse au message
