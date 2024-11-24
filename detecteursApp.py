import sys, os
import rpiMethodes
import RedisInOut as redisInOut
from dataclasses import dataclass


redisIpAdresse="192.168.1.210"
redisInOut.InitialiseRedisClient(redisIpAdresse)

class const:
    format = "02-01-2006 15:04:05"



@dataclass
class DETECTEUR:
    MouvChambrePrincipale: int=0
    MouvChambreSecondaire: int=0
    MouvBureau: int=0
    MouvSalon: int=0
    MouvSalleBillard: int=0
    MouvSalleVernis: int=0
    InterPorteAvant: int=0
    InterPorteArriere: int=0
    InterPorteSousSol: int=0
    DectEauAtelier: int=0
    DectEauSalleLavage: int=0
    DectEauPluie: int=0
    DectFumeeSalleBillard: int=0
    DectFumeeAtelier: int=0


@dataclass
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False

detecteurGicleur = dict()
requete=""
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

    if requete == "Gicleur_2_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais1", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_2_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais1", False)    
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_3_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais1", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_3_OFF":
        print ("-------------------- OFF")
        rpiMethodes.set_relais("relais1", False)    
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_4_ON":
        print ("--------------------- ON")
        rpiMethodes.set_relais("relais1", True)
        redisInOut.setRequeteArrosageNil()

    if requete == "Gicleur_4_OFF":
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
            print ("passe 3 ")
            detecteurAlarme=rpiMethodes.getValeursAlarme(detecteurAlarme)
            print ("passe 4 ")
            redisInOut.publishInterfaceAlarmeDetecteur(detecteurAlarme)
            # pour systeme arrosage va lire si le systeme arrose
            gicleursStatut=rpiMethodes.getValeursGicleurs(gicleursStatut)

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
