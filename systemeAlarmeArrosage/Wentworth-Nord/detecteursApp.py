
import sys, os
import rpiMethodes
import RedisInOut as redisInOut
from dataclasses import dataclass


redisIpAdresse="192.168.1.143"
redisInOut.InitialiseRedisClient(redisIpAdresse)

class const:
    format = "02-01-2006 15:04:05"
  
    fumeePin                       = 16
    mouvementPin                   = 23
    eauElectriquePin               = 24
    eauTraitementPin               = 25
    panneElectriquePin             = 5


detecteurGicleur = dict()
requete=""

@dataclass
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False


@dataclass
class DETECTEUR:
    Prop: float = 0.0
    Co: float = 0.0
    Fumee: float = 0.0
    Mouvement: float = 0.0
    EauElectrique: float = 0.0
    EauTraitement: float = 0.0
    PanneElectrique: float = 0.0



def detecteurDataStructure(dectArduino):
    global detecteurAlarme
    detecteurAlarme = DETECTEUR()

    detecteurAlarme.Prop=dectArduino["Prop"]
    detecteurAlarme.Co=dectArduino["Co"]
    detecteurAlarme.Fumee=dectArduino["Fumee"]
    detecteurAlarme.Mouvement=dectArduino["Mouvement"]
    detecteurAlarme.EauElectrique=dectArduino["EauElectrique"]
    detecteurAlarme.EauTraitement=dectArduino["EauTraitement"]
    detecteurAlarme.PanneElectrique=dectArduino["PanneElectrique"]

    return detecteurAlarme

def initialiseGicleursStatut(**gicleursStatut):
    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 1
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 2
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 3
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 4
    gicleurRec.Statut = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec
    
    return gicleursStatut


def executeRequete(requete):
    print ("requete arrosage 1 ", requete)
    if requete == "Gicleur_1_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais1", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_1_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais1", False)    
        redisInOut.setRequeteArrosageNil()


redisInOut.StartSystemeArrosageRequete()

if __name__ == '__main__':

    gicleursStatut = dict()
    gicleursStatut = initialiseGicleursStatut()

    detecteurAlarme=DETECTEUR()

    while True:
        try:

            # pour alarmes
            DetecteuAlarme=rpiMethodes.getAlarmeDetecteur(detecteurAlarme, const.fumeePin,const.mouvementPin, const.eauElectriquePin,const.eauTraitementPin,const.panneElectriquePin)
            redisInOut.publishInterfaceAlarmeDetecteur(detecteurAlarme)

            # pour systeme arrosage va lire si le systeme arrose
            gicleursStatut=rpiMethodes.getArrosageDetecteur(gicleursStatut)

            requete=redisInOut.getRequeteArrosage()
            redisInOut.setRequeteArrosageNil()
            if requete != "1" and  requete != "":
                executeRequete(requete)
            
            redisInOut.publishInterfaceDetecteurArrosage(gicleursStatut)  

        except Exception as e:
            print (e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)
