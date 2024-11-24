
import sys, os
from time import sleep
from json import JSONEncoder
from dataclasses import dataclass
import threading
from datetime import datetime, timedelta
import socket,pickle
from time import sleep
import struct
import RedisInOut as redisInOut
import socket
import systemeArrosageDataClass as dc

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print (hostname)
if hostname=="raspiMontreal":
    import rpiMethodesMontreal as rpiMethodes
else:
    if hostname=="raspiWentworthNord":
        import rpiMethodesWentworthNord as rpiMethodes

redisIpAdresse=IPAddr

redisInOut.InitialiseRedisClient(redisIpAdresse)

NoZone=0
ZoneNom=""
TempsArrosage=False
ArrosageEnCour=False
ArrosageDemarre=False
ArrosageTermine=False
systemeArrosageEnCour=False
NombreJourInterval=2
ZoneActive=False
ZonePhysique=""
Affichage=False
AffichageWeb=False
MessageErreur=""
ValeurPluie=0
DateHeureCourante =datetime
DateHeureDebutArrosage = datetime
DateHeureDebutIntervalle = datetime
Message=""
reset6Heures = False

class const:
    format = "02-01-2006 15:04:05"
    nombreCourrielEnvoye           = 1
    zoneInactive                   = -1
    zoneActive                     = 1
    valeurNulle                    = -1
    dureeUpload                    = 1  # devrait être 60 minutes
    dureeCourriel                  = 60 #  secondes
    dureeRaspberryErreur           = 5
    dureeSauveFichier              = 1
    heureTestMatin                 = 7
    dureeThreadConnexion           = 15 # 15 minutes
    dureeVerifieThreadConnexion    = 2  # 2 minutes
    dureeuploadToScreen            = 1  # nb de seconde pour envoyer a l ecran
    HIGH                           = 1
    LOW                            = 0
    nombreCourrielQuotidien        = 5


# @dataclass
# class MESSAGES_ACTIVITES:
#     DateMessage: datetime = datetime.now()
#     NoZone: int= 0
#     Message: str = ""
# 
# 
# @dataclass
# class GICLEURS:
#     NoZone: int = 0
#     ZoneNom: str = ""
#     ZonePhysique: str = ""
#     ZoneActive: bool = False
#     TempsArrosage: int = 0
#     Affichage: bool = False
#     AffichageWeb: bool = False
#     MessageErreur: str = ""
# 
# @dataclass
# class ARROSAGE_DATA:
#     NoZone: int = 0
#     TempsArrosage: int = 0
#     ArrosageEnCour: bool = False
#     ArrosageTermine: bool = False
# 
# @dataclass
# class CONFIGURATION_GENERALE:
#     HeureDebutArrosage: str = ""   
#     SystemArrosageActif: bool = False         
#     SondePluieActive: bool = False           
#     ArrosageJourPairImpair: str = ""
#     NombreJourInterval: int = 0    
# 
# @dataclass
# class GICLEURS_STATUT:  
#     NoZone: int = 0
#     Statut: bool = False
# 
# @dataclass
# class GICLEUR_EN_COUR:  
#     NoZone: int = 0  
#     HeureDepartArrosage: int = 0  


# pour info
def initializeDonneesGenerales(**donneesArrosage):
    donneesGeneralesRec=dc.ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="1"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=dc.ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="2"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=dc.ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="3"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=dc.ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="4"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec
    return donneesArrosage

def initialiseGicleursStatut(**gicleursStatut):
    gicleurRec = dc.GICLEURS_STATUT()
    gicleurRec.NoZone = 1
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = dc.GICLEURS_STATUT()
    gicleurRec.NoZone = 2
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = dc.GICLEURS_STATUT()
    gicleurRec.NoZone = 3
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = dc.GICLEURS_STATUT()
    gicleurRec.NoZone = 4
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec
    
    return gicleursStatut



def sauvegardeMessageActivites(DateMessage,NoZone,Message):
    
    messageActivite = dc.MESSAGES_ACTIVITES(DateHeureCourante, NoZone, Message)
    messageActivite.DateMessage=DateMessage
    messageActivite.NoZone=NoZone
    messageActivite.Message=Message
    
    redisInOut.sauvegardeMessageSystemeArrosage(messageActivite)
    
        
# def recupereRapportActivitesArrosage():
# 
#     activites = []
#     with open(directory + '/activiteArrosage.data', 'rb') as fr:
#         try:
#             while True:
#                 activites.append(pickle.load(fr))
#         except EOFError:
#             pass
#     # SendRapportActivitesArrosage(SendRec["RapportActivitesArrosage"].Ip, SendRec["RapportActivitesArrosage"].Port, activites)
    
    
def arrosageValide():
    global ValeurPluie
    global confGeneral
    global DateHeureDebutIntervalle
    global ArrosageDemarre

    valide=False
    jourValide=False
    dateHeureValide=False
    DateHeureCourante=datetime.now()
    pluieValide=False

    if DateHeureCourante.day  % 2 == 0 and confGeneral.ArrosageJourPairImpair=="Pair":
        jourValide=True
    else:
        if DateHeureCourante.day  % 2 != 0 and confGeneral.ArrosageJourPairImpair=="Impair":
            jourValide=True
            #sauvegardeMessageLogs("Systeme arrosage Montreal heure et jour impair pair : " + str(jourValide))
        else:
            jourValide=False

    if confGeneral.SystemArrosageActif==True:
        if confGeneral.SondePluieActive==False:
            pluieValide=True

        if pluieValide==True and confGeneral.HeureDebutArrosage==DateHeureCourante.hour and jourValide==True and (datetime.now() - DateHeureDebutIntervalle).days >= confGeneral.NombreJourInterval:
           valide=True
        else:
            valide=False

        
    # print ("Nombre de jour interval pour l arrosage : ", valide, (datetime.now() - DateHeureDebutIntervalle).days, confGeneral.NombreJourInterval)  

    return valide



def initialiseConfigurationGenerale():
    global GicleurAssocie
    confGeneral=dc.CONFIGURATION_GENERALE()

    confGeneral.ArrosageJourPairImpair="Pair"
    confGeneral.SystemArrosageActif=True
    confGeneral.SondePluieActive=False
    confGeneral.HeureDebutArrosage=4
    confGeneral.NombreJourInterval

    return confGeneral


def initialiaseGicleurs(**gicleurs):
    gicleurRec=dc.GICLEURS()
    gicleurRec.NoZone=1
    gicleurRec.ZoneNom="relais1"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la rue"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=dc.GICLEURS()
    gicleurRec.NoZone=2
    gicleurRec.ZoneNom="relais2"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Arrière Ail"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec   

    gicleurRec=dc.GICLEURS()
    gicleurRec.NoZone=3
    gicleurRec.ZoneNom="relais3"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la maison et le coté"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=dc.GICLEURS()
    gicleurRec.NoZone=4
    gicleurRec.ZoneNom="relais4"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Arrière coté de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    GicleurAssocie={}
    
    return gicleurs


# hostname=socket.gethostname()  
# SendRec["ArrosageEcranDataEquipement"].Ip=socket.gethostbyname(hostname)  
  
def decodeDataDetecteur(gicleurValeurList, **gicleursStatut):

    recGicleur=dc.GICLEURS_STATUT()
    recGicleur = gicleursStatut["1"]
    recGicleur.Statut = gicleurValeurList[0]
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["1"]=recGicleur

    recGicleur=dc.GICLEURS_STATUT()
    recGicleur = gicleursStatut["2"]
    recGicleur.Statut = gicleurValeurList[1]
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["2"]=recGicleur

    recGicleur=dc.GICLEURS_STATUT()
    recGicleur = gicleursStatut["3"]
    recGicleur.Statut = gicleurValeurList[2]
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["3"]=recGicleur

    recGicleur=dc.GICLEURS_STATUT()
    recGicleur = gicleursStatut["4"]
    recGicleur.Statut = gicleurValeurList[3]
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["4"]=recGicleur
    
    return gicleursStatut


def sendSystemeArrosageGicleursStatuts():
    global gicleursStatut
    while True:
        redisInOut.publishSystemeStatutGicleurs(gicleursStatut)
        sleep(1)

def fermerGicleurs(gicleurs):
    if gicleurs["1"].ZoneActive==True:
        rpiMethodes.set_relais(1, False)   # arrête les gicleurs
    if gicleurs["2"].ZoneActive==True:
        rpiMethodes.set_relais(2, False)   # arrête les gicleurs
    if gicleurs["3"].ZoneActive==True:
        rpiMethodes.set_relais(3, False)   # arrête les gicleurs
    if gicleurs["4"].ZoneActive==True:
        rpiMethodes.set_relais(4, False)   # arrête les gicleurs
    
def executeRequete(Requete):
    global gicleurs,confGeneral
    
    if Requete!="":
        redisInOut.setRequeteArrosageNil()            
        sleep(1)    
    
    if Requete == "NouvelleConfiguration":
        sauvegardeMessageActivites(datetime.now(),"config general et gicleurs", "Changement de configuration")
        confGeneral = redisInOut.recupereSystemeArrosageConfigurationGenerale()
        gicleurs=redisInOut.recupereArrosageConfigurationGicleurs()
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "recupereRapportActivitesArrosage":
        # recupereRapportActivitesArrosage()
        sleep(.3)
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurSet1" and gicleurs["1"].ZoneActive==True:
        dataRec=donneesArrosage["1"]
        dataRec.ArrosageTermine=True
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurReSet1" and gicleurs["1"].ZoneActive==True:
        dataRec=donneesArrosage["1"]
        dataRec.ArrosageTermine=False
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurSet2" and gicleurs["1"].ZoneActive==True:
        dataRec=donneesArrosage["2"]
        dataRec.ArrosageTermine=True
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurReSet2" and gicleurs["2"].ZoneActive==True:
        dataRec=donneesArrosage["2"]
        dataRec.ArrosageTermine=False
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurSet3" and gicleurs["3"].ZoneActive==True:
        dataRec=donneesArrosage["3"]
        dataRec.ArrosageTermine=True
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurReSet3" and gicleurs["3"].ZoneActive==True:
        dataRec=donneesArrosage["3"]
        dataRec.ArrosageTermine=False
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurSet4" and gicleurs["4"].ZoneActive==True:
        dataRec=donneesArrosage["4"]
        dataRec.ArrosageTermine=True
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "GicleurReSet4" and gicleurs["4"].ZoneActive==True:
        dataRec=donneesArrosage["4"]
        dataRec.ArrosageTermine=False
        sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        Requete=""
        redisInOut.setRequeteArrosageNil()
    elif Requete == "Gicleur_1_ON" and ArrosageEnCour==False and gicleurs["1"].ZoneActive==True:
        rpiMethodes.set_relais("1", True)   # ouvre le gicleur pour arrosage
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 1 ", "Gicleur_1_ON")
    elif Requete == "Gicleur_1_OFF" and gicleurs["1"].ZoneActive==True:
        rpiMethodes.set_relais("1", False)   # arrête les gicleurs
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 1 ", "Gicleur_1_OFF")
    elif Requete == "Gicleur_2_ON" and ArrosageEnCour==False and gicleurs["2"].ZoneActive==True:
        rpiMethodes.set_relais("2", True)   # ouvre le gicleur pour arrosage
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 2 ", "Gicleur_2_ON")
    elif Requete == "Gicleur_2_OFF" and gicleurs["2"].ZoneActive==True:
        rpiMethodes.set_relais("2", False)   # arrête les gicleurs
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 2 ", "Gicleur_2_OFF")
    elif Requete == "Gicleur_3_ON" and ArrosageEnCour==False and gicleurs["3"].ZoneActive==True:
        rpiMethodes.set_relais("3", True)   # ouvre le gicleur pour arrosage
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 3 ", "Gicleur_3_ON")
    elif Requete == "Gicleur_3_OFF" and gicleurs["3"].ZoneActive==True:
        rpiMethodes.set_relais("3", False)   # arrête les gicleurs
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 3 ", "Gicleur_3_OFF")
    elif Requete == "Gicleur_4_ON" and ArrosageEnCour==False and gicleurs["4"].ZoneActive==True:
        rpiMethodes.set_relais("4", True)   # ouvre le gicleur pour arrosage
        Requete=""
        # redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 4 ", "Gicleur_4_ON")
    elif Requete == "Gicleur_4_OFF" and gicleurs["4"].ZoneActive==True:
        rpiMethodes.set_relais("4", False)   # arrête les gicleurs
        Requete=""
        redisInOut.setRequeteArrosageNil()
        sauvegardeMessageActivites(datetime.now()," Zone 4 ", "Gicleur_4_OFF")

Requete=""


donneesArrosage=dict()
donneesArrosage=initializeDonneesGenerales(**donneesArrosage)
gicleurEnCour = dc.GICLEUR_EN_COUR()
gicleursStatut=dict()
gicleursStatut=initialiseGicleursStatut()


confGeneral=dict()
# confGeneral=initialiseConfigurationGenerale()
# redisInOut.sauvegardeSystemeArrosageConfigurationGenerale(confGeneral)

gicleurs=dict()
gicleurs=initialiaseGicleurs()
# redisInOut.sauvegardeArrosageConfigurationGicleurs(gicleurs)


confGeneral = redisInOut.recupereSystemeArrosageConfigurationGenerale()
gicleurs=redisInOut.recupereArrosageConfigurationGicleurs()
rpiMethodes.initialiseRelaisGicleur(gicleurs)  # initialise gicleur sur le raspberry pi

# redisInOut.StartSystemeArrosageRequete()

fermerGicleurs(gicleurs)

if __name__ == '__main__':
    global valeurPluie

    DateHeureCourante=datetime.now()
    DateHeureDebutIntervalle=datetime.now() + timedelta(days=-10)

    sauvegardeMessageActivites(datetime.now(),"Systeme arrosage Montreal", "systeme demarre" )

    # t1 = threading.Thread(target=sendSystemeArrosageGicleursStatuts)
    # t1.start()

    
    while True :  
        try:
            redisInOut.RunRedisInOut("StartSystemeArrosageRequete")    # check if task is running        
            gicleurValeurList = rpiMethodes.getValeursGicleurs(gicleurs) 
            gicleursStatut=decodeDataDetecteur(gicleurValeurList, **gicleursStatut)
            redisInOut.publishSystemeStatutGicleurs(gicleursStatut)
            
            Requete = redisInOut.getRequeteArrosage()
            sleep(1)
            executeRequete(Requete)
            Requete=""
 

            for rec in donneesArrosage:
                dataRec=dc.ARROSAGE_DATA()
                dataRec=donneesArrosage[rec]
                
                # print (" valeurs : ",  dataRec.NoZone, ArrosageDemarre==False , dataRec.ArrosageTermine==False , dataRec.ArrosageEnCour==False , systemeArrosageEnCour==False , gicleurs[rec].ZoneActive==True, arrosageValide())
                if  arrosageValide()==True and dataRec.ArrosageTermine==False and dataRec.ArrosageEnCour==False and systemeArrosageEnCour==False and gicleurs[rec].ZoneActive==True:
                    # depart du gicleur
                    dataRec.ArrosageEnCour=True
                    systemeArrosageEnCour=True          
                    ArrosageDemarre=True
                    gicleurEnCour.HeureDepartArrosage=datetime.now()
                    gicleurEnCour.NoZone=dataRec.NoZone
                    DateHeureDebutArrosage=datetime.now()
                    rpiMethodes.set_relais(dataRec.NoZone, True)   # ouvre le gicleur pour arrosage
                    print(" arrosage demarrer ", dataRec.NoZone)
                    sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage en cours" )
                    sleep(1)
                    donneesArrosage[dataRec.NoZone]=dataRec
                    reset6Heures=False
                    break
            

                # print ( systemeArrosageEnCour==True, (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds > 10, gicleurs[str(gicleurEnCour.NoZone)].TempsArrosage)
                if systemeArrosageEnCour==True and (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds > 10:
    # 
                    if (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds/60 >= int(gicleurs[str(gicleurEnCour.NoZone)].TempsArrosage):
                        # arret du gicleur

                        dataRec=dc.ARROSAGE_DATA()
                        dataRec=donneesArrosage[gicleurEnCour.NoZone]
                        dataRec.ArrosageTermine=True
                        dataRec.ArrosageEnCour=False
                        systemeArrosageEnCour=False
                        print(" arrosage arrete  ", dataRec.NoZone)
                        rpiMethodes.set_relais(dataRec.NoZone, False)   # arrête les gicleurs
                        sleep(1)
                        sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage terminé" )

                        # sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) +"  Arrosage terminé")
                        donneesArrosage[dataRec.NoZone]=dataRec

            
            if datetime.now().hour == 3 and reset6Heures == False:
                for rec in donneesArrosage:
                    dataRec=dc.ARROSAGE_DATA()
                    dataRec=donneesArrosage[rec]
                    dataRec.ArrosageTermine=False 
                    dataRec.ArrosageEnCour=False
                    donneesArrosage[rec]=dataRec
                sauvegardeMessageActivites(datetime.now(),1-4, "Reset des gicleurs" )
                sleep(1)
                # sauvegardeMessageLogs("Systeme arrosage Montreal :" + " gicleurs reset 6 heures")
                DateHeureDebutIntervalle=datetime.now() + timedelta(days=-1)
                reset6Heures=True
                #sleep(3)
            # print (" ip a envoyer  ", SendRec["ArrosageEcranDataEquipement"].Ip)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
