
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

redisIpAdresse="192.168.1.143"
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


@dataclass
class MESSAGES_ACTIVITES:
    DateMessage: datetime = datetime.now()
    NoZone: int= 0
    Message: str = ""
@dataclass
class DETECTEUR_GICLEUR:
    noZone: int = 0
    gicleurStatut: bool = False

@dataclass
class GICLEURS:
    NoZone: int = 0
    ZoneNom: str = ""
    ZonePhysique: str = ""
    ZoneActive: bool = False
    TempsArrosage: int = 0
    Affichage: bool = False
    AffichageWeb: bool = False
    MessageErreur: str = ""

@dataclass
class ARROSAGE_DATA:
    NoZone: int = 0
    TempsArrosage: int = 0
    ArrosageEnCour: bool = False
    ArrosageTermine: bool = False

@dataclass
class CONFIGURATION_GENERALE:
    HeureDebutArrosage: str = ""   
    SystemArrosageActif: bool = False         
    SondePluieActive: bool = False           
    ArrosageJourPairImpair: str = ""
    NombreJourInterval: int = 0    

@dataclass
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False

@dataclass
class GICLEUR_EN_COUR:  
    NoZone: int = 0  
    HeureDepartArrosage: int = 0  

@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""



def initializeDonneesGenerales(**donneesArrosage):
    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="1"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="2"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="3"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="4"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec
    return donneesArrosage

# def initialiseGicleursStatut(**gicleursStatut):
#     gicleurRec = GICLEURS_STATUT()
#     gicleurRec.NoZone = 1
#     gicleurRec.Statut = 0
#     gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec
# 
#     gicleurRec = GICLEURS_STATUT()
#     gicleurRec.NoZone = 2
#     gicleurRec.Statut = 0
#     gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec
# 
#     gicleurRec = GICLEURS_STATUT()
#     gicleurRec.NoZone = 3
#     gicleurRec.Statut = 0
#     gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec
# 
#     gicleurRec = GICLEURS_STATUT()
#     gicleurRec.NoZone = 4
#     gicleurRec.Statut = 0
#     gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec
#     
#     return gicleursStatut


def sauvegardeMessageLogs(DataLOG):
    print (DataLOG)


# def sauvegardeMessageActivites(DateMessage,NoZone,Message):
#     
#     messageActivite = MESSAGES_ACTIVITES(DateHeureCourante, NoZone, Message)
#     messageActivite.DateMessage=DateMessage
#     messageActivite.NoZone=NoZone
#     messageActivite.Message=Message
#     print (messageActivite)
#     with open(directory + '/activiteArrosage.data', 'ab+') as fp:
#        pickle.dump(messageActivite,fp)
#        print("sauvegarde message activite")
#         
# def recupereRapportActivitesArrosage():
# 
#     activites = []
#     with open(directory + '/activiteArrosage.data', 'rb') as fr:
#         try:
#             while True:
#                 activites.append(pickle.load(fr))
#         except EOFError:
#             pass
#     SendRapportActivitesArrosage(SendRec["RapportActivitesArrosage"].Ip, SendRec["RapportActivitesArrosage"].Port, activites)

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

        
    print ("Nombre de jour interval pour l arrosage : ", valide, (datetime.now() - DateHeureDebutIntervalle).days, confGeneral.NombreJourInterval)  

    return valide



def FermerGicleurs():
        print("passe 20")
        redisInOut.publishInterfaceRequete("Gicleur_1_OFF")
        # redisInOut.publishInterfaceRequete("Gicleur_2_OFF")     
        # redisInOut.publishInterfaceRequete("Gicleur_3_OFF")     
        # redisInOut.publishInterfaceRequete("Gicleur_4_OFF")     
        print ("passe 22")
        sleep (.5)

def initialiseConfigurationGenerale():
    global GicleurAssocie
    confGeneral=CONFIGURATION_GENERALE()

    confGeneral.ArrosageJourPairImpair="Pair"
    confGeneral.SystemArrosageActif=True
    confGeneral.SondePluieActive=False
    confGeneral.HeureDebutArrosage=13
    confGeneral.NombreJourInterval

    return confGeneral


def initialiaseGicleurs(**gicleurs):
    gicleurRec=GICLEURS()
    gicleurRec.NoZone=1
    gicleurRec.ZoneNom="relais1"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la rue"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=2
    gicleurRec.ZoneNom="relais2"
    gicleurRec.ZoneActive=False
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Arrière Ail"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec   

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=3
    gicleurRec.ZoneNom="relais3"
    gicleurRec.ZoneActive=False
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la maison et le coté"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=4
    gicleurRec.ZoneNom="relais4"
    gicleurRec.ZoneActive=False
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
  
def decodeDataDetecteur(relaiValeur, **gicleursStatut):


    recGicleur=GICLEURS_STATUT()
    recGicleur = gicleursStatut["1"]
    recGicleur.Statut = relaiValeur

    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["1"]=recGicleur

    recGicleur = gicleursStatut["2"]
    recGicleur.Statut = relaiValeur
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["2"]=recGicleur

    recGicleur = gicleursStatut["3"]
    recGicleur.Statut = relaiValeur
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["3"]=recGicleur

    recGicleur = gicleursStatut["4"]
    recGicleur.Statut = relaiValeur
    recGicleur.DateHeureCourante = datetime.now()
    if recGicleur.Statut==0:
        recGicleur.Statut=1
    else:
        recGicleur.Statut=0
    gicleursStatut["4"]=recGicleur

    return gicleursStatut


def sauvegardeMessageActivites(Message):
    print ("En construction")

def sendSystemeArrosageGicleursStatuts():
    global gicleursStatut
    while True:
        redisInOut.publishSystemeStatutGicleurs(gicleursStatut)
        sleep(1)


Requete=""

confGeneral=dict()
donneesArrosage=dict()
donneesArrosage=initializeDonneesGenerales(**donneesArrosage)
gicleurs=dict()
gicleurEnCour = GICLEUR_EN_COUR()
gicleursStatut=dict()

confGeneral=initialiseConfigurationGenerale()
# redisInOut.sauvegardeSystemeArrosageConfigurationGenerale(confGeneral)
gicleurs = initialiaseGicleurs()
# redisInOut.sauvegardeArrosageConfigurationGicleurs(gicleurs)

redisInOut.StartSystemeArrosageRequete()
redisInOut.startSystemeStatutGicleur()


if __name__ == '__main__':
    global valeurPluie

    confGeneral = redisInOut.recupereSystemeArrosageConfigurationGenerale()
    gicleurs=redisInOut.recupereArrosageConfigurationGicleurs()
    DateHeureCourante=datetime.now()
    DateHeureDebutIntervalle=datetime.now() + timedelta(days=-10)

    sauvegardeMessageLogs("Systeme arrosage Montreal :" + "systeme demarre" )

    t1 = threading.Thread(target=sendSystemeArrosageGicleursStatuts)
    t1.start()

    FermerGicleurs()
    
    while True :  
        try:
            gicleursStatut= redisInOut.getSystemeArrosageStatut()
            redisInOut.RunRedisInOut("StartSystemeArrosageRequete")    # check if task is running
            
            Requete = redisInOut.getRequeteArrosage()
            sleep(1)
            if Requete!="":
                print ("allo  xxxxxxx  ",Requete)
                redisInOut.setRequeteArrosageNil()
              
            sleep(1)    

           
            gicleurValideRec = redisInOut.getSystemeArrosageStatut()
            gicleursStatut=decodeDataDetecteur(gicleurValideRec, **gicleursStatut)

            redisInOut.publishSystemeStatutGicleurs(gicleursStatut)
            
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
            elif Requete == "GicleurSet1":
                dataRec=donneesArrosage["1"]
                dataRec.ArrosageTermine=True
                # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
                Requete=""
                redisInOut.setRequeteArrosageNil()
            elif Requete == "GicleurReSet1":
                dataRec=donneesArrosage["1"]
                dataRec.ArrosageTermine=False
                # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
                Requete=""
                redisInOut.setRequeteArrosageNil()
            # elif Requete == "GicleurSet2":
            #     dataRec=donneesArrosage["2"]
            #     dataRec.ArrosageTermine=True
            #     # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            # elif Requete == "GicleurReSet2":
            #     dataRec=donneesArrosage["2"]
            #     dataRec.ArrosageTermine=False
            #     # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            # elif Requete == "GicleurSet3":
            #     dataRec=donneesArrosage["3"]
            #     dataRec.ArrosageTermine=True
            #     # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            # elif Requete == "GicleurReSet3":
            #     dataRec=donneesArrosage["3"]
            #     dataRec.ArrosageTermine=False
            #     # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            # elif Requete == "GicleurSet4":
            #     dataRec=donneesArrosage["4"]
            #     dataRec.ArrosageTermine=True
            #     # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            # elif Requete == "GicleurReSet4":
            #     dataRec=donneesArrosage["4"]
            #     dataRec.ArrosageTermine=False
            #     # sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            elif Requete == "Gicleur_1_ON" and ArrosageEnCour==False:
                redisInOut.publishInterfaceRequete("Gicleur_1_ON")
                Requete=""
                redisInOut.setRequeteArrosageNil()
                # sauvegardeMessageActivites(datetime.now()," Zone 1 ", "Gicleur_1_ON")
            elif Requete == "Gicleur_1_OFF":
                redisInOut.publishInterfaceRequete("Gicleur_1_OFF")
                Requete=""
                redisInOut.setRequeteArrosageNil()
                # sauvegardeMessageActivites(datetime.now()," Zone 1 ", "Gicleur_1_OFF")
            # elif Requete == "Gicleur_2_ON" and ArrosageEnCour==False:
            #     redisInOut.publishInterfaceArduinoRequete("Gicleur2_ON")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            #     # sauvegardeMessageActivites(datetime.now()," Zone 2 ", "Gicleur_2_ON")
            # elif Requete == "Gicleur_2_OFF":
            #     redisInOut.publishInterfaceArduinoRequete("Gicleur_2_OFF")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            #     # sauvegardeMessageActivites(datetime.now()," Zone 2 ", "Gicleur_2_OFF")
            # elif Requete == "Gicleur_3_ON" and ArrosageEnCour==False:
            #     redisInOut.publishInterfaceArduinoRequete("Gicleur_3_ON")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            #     # sauvegardeMessageActivites(datetime.now()," Zone 3 ", "Gicleur_3_ON")
            # elif Requete == "Gicleur_3_OFF":
            #     redisInOut.publishInterfaceArduinoRequete("Gicleur_3_OFF")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            #     # sauvegardeMessageActivites(datetime.now()," Zone 3 ", "Gicleur_3_OFF")
            # elif Requete == "Gicleur_4_ON" and ArrosageEnCour==False:
            #     redisInOut.publishInterfaceArduinoRequete("Gicleur_4_ON")
            #     Requete=""
            #     # redisInOut.setRequeteArrosageNil()
            #     # sauvegardeMessageActivites(datetime.now()," Zone 4 ", "Gicleur_4_ON")
            # elif Requete == "Gicleur_4_OFF":
            #     redisInOut.publishInterfaceArduinoRequete("Gicleur_4_OFF")
            #     Requete=""
            #     redisInOut.setRequeteArrosageNil()
            #     # sauvegardeMessageActivites(datetime.now()," Zone 4 ", "Gicleur_4_OFF")
            print ("passe 5")

            for rec in donneesArrosage:
                dataRec=ARROSAGE_DATA()
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
                    redisInOut.publishSystemeArrosageRequete("Gicleur_1_ON")
                    # sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage en cours" )
                    sleep(1)
                    donneesArrosage[dataRec.NoZone]=dataRec
                    reset6Heures=False
                    break
            

                print ( systemeArrosageEnCour==True, (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds > 10, gicleurs[str(gicleurEnCour.NoZone)].TempsArrosage)
                if systemeArrosageEnCour==True and (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds > 10:
    # 
                    if (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds/60 >= int(gicleurs[str(gicleurEnCour.NoZone)].TempsArrosage):
                        # arret du gicleur

                        dataRec=ARROSAGE_DATA()
                        dataRec=donneesArrosage[gicleurEnCour.NoZone]
                        dataRec.ArrosageTermine=True
                        dataRec.ArrosageEnCour=False
                        systemeArrosageEnCour=False
                        redisInOut.publishSystemeArrosageRequete("Gicleur_1_OFF")
                        sleep(.5)
                        # sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage terminé" )
                        sleep(2)
                        sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) +"  Arrosage terminé")

                        donneesArrosage[dataRec.NoZone]=dataRec

            
            if datetime.now().hour == 3 and reset6Heures == False:
                for rec in donneesArrosage:
                    dataRec=ARROSAGE_DATA()
                    dataRec=donneesArrosage[rec]
                    dataRec.ArrosageTermine=False 
                    dataRec.ArrosageEnCour=False
                    donneesArrosage[rec]=dataRec
                # sauvegardeMessageActivites(datetime.now(),1-4, "Reset des gicleurs" )
                sleep(1)
                sauvegardeMessageLogs("Systeme arrosage Montreal :" + " gicleurs reset 6 heures")
                DateHeureDebutIntervalle=datetime.now() + timedelta(days=-1)
                reset6Heures=True
                #sleep(3)
            # print (" ip a envoyer  ", SendRec["ArrosageEcranDataEquipement"].Ip)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
