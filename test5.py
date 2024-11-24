from datetime import datetime, timedelta
import socket,pickle
from time import sleep
import struct
from dataclasses import dataclass
import RedisInOut as red
import redis
import jsonpickle
import systemeArrosageDataClass as dc
# @dataclass
# class MESSAGES_ACTIVITES:
#     DateMessage: datetime = datetime.now()
#     NoZone: int= 0
#     Message: str = ""
    
messages=[]

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print (hostname)
if hostname=="raspiMontreal":
    import rpiMethodesMontreal as rpiMethodes
else:
    if hostname=="raspiWentworthNord":
        import rpiMethodesWentworthNord as rpiMethodes

redisIpAdresse=IPAddr

red.InitialiseRedisClient(redisIpAdresse)
data = {}

if __name__ == '__main__':
    global valeurPluie

    DateHeureCourante=datetime.now()
    messageRec=dc.MESSAGES_ACTIVITES()
    messageRec.DateMessage=str(DateHeureCourante)
    messageRec.NoZone=1
    messageRec.Message="asdfdllasldflasdf"
    red.sauvegardeMessageSystemeArrosage(messageRec)
    
    xxx = red.recupereMessageSystemeArrosage("systemeArrosageMessage")
    # print ("---------------------- ",xxx)
    

    for keys in xxx:
        messageRec = jsonpickle.decode(xxx[keys])
        print (messageRec.DateMessage)
        print (messageRec.NoZone)
        print (messageRec.Message)        


    
    # for key in xxx:
    #     print(key)
    #     
    #     values = map(str, xxx.get(key))
    #     kv = zip(key, values)
    #     print (key, values)