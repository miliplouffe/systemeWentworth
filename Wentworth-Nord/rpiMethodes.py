import sys, os
from time import sleep
from json import JSONEncoder
import gpiozero
from gpiozero import DigitalInputDevice
from gpiozero import LED

class const:
    detecteurFumee=16
    detecteurMouvement=23
    detecteurEauElectrique=24
    detecteurEauTraitement=25
    detecteurPanneElectrique=5


gicleur0 = gpiozero.OutputDevice(0, active_high=False, initial_value=False)
gicleur1=  gpiozero.OutputDevice(4, active_high=False, initial_value=False)
gicleur2=gicleur0
gicleur3=gicleur0
gicleur4=gicleur0

detecteurFumee = DigitalInputDevice(const.detecteurFumee,pull_up=True)
detecteurMouvement = DigitalInputDevice(const.detecteurMouvement,pull_up=True)
detecteurEauElectrique = DigitalInputDevice(const.detecteurEauElectrique,pull_up=True)
detecteurEauTraitement = DigitalInputDevice(const.detecteurEauTraitement,pull_up=True)
detecteurPanneElectrique = DigitalInputDevice(const.detecteurPanneElectrique,pull_up=True)


def get_relais(nomRelais):
    global gicleur1, gicleur2, gicleur3, gicleur4

    valeur=False

    if nomRelais=="gicleur1":
       valeur= gicleur1.value
    if nomRelais=="gicleur2":
        valeur= gicleur2.value
    if nomRelais=="gicleur3":
        valeur= gicleur3.value            
    if nomRelais=="gicleur4":
        valeur= gicleur4.value
    
    return valeur

def initialiseRelaisGicleur(gicleurs):
    global gicleur1, gicleur2, gicleur3,gicleur4
    if gicleurs["1"].ZoneActive==True:
        gicleur1.on()
    if gicleurs["2"].ZoneActive==True:
        gicleur2.on()
    if gicleurs["3"].ZoneActive==True:
        gicleur3.on()
    if gicleurs["4"].ZoneActive==True:
        gicleur4.on()


def set_relais(nomRelais, statut):
    global relais1, relais2, relais3, relais4

    if statut==True:
        print ("statut True")
        if nomRelais =="1":
            gicleur1.off()
        if nomRelais =="2":
            gicleur2.off()        
        if nomRelais =="3":
            gicleur3.off()
        if nomRelais =="4":
            gicleur4.off()            
    else:
        gicleur1.on()
        gicleur2.on()
        gicleur3.on()
        gicleur4.on()


    PanneElectrique: float = 0.0

def getAlarmeDetecteur(detecteurAlarme):
    global detecteurFumee,detecteurMouvement,detecteurEauElectrique,detecteurEauTraitement,detecteurPanneElectrique

    detecteurAlarme.Prop=-1.0
    detecteurAlarme.Co=-1.0
    detecteurAlarme.Fumee =  detecteurFumee.value
    detecteurAlarme.Mouvement=  detecteurMouvement.value
    detecteurAlarme.EauTraitement = detecteurEauTraitement.value
    detecteurAlarme.EauElectrique = detecteurEauElectrique.value
    detecteurAlarme.PanneElectrique = detecteurPanneElectrique.value

    return detecteurAlarme

def getValeursGicleurs(gicleurs):
    equipementsGicleurs=[]
    if gicleurs["1"].ZoneActive==True:
        equipementsGicleurs.append(gicleur1.value)
    else:
         equipementsGicleurs.append(-1)
    if gicleurs["2"].ZoneActive==True:
        equipementsGicleurs.append(gicleur1.value)
    else:
         equipementsGicleurs.append(-1)        
    if gicleurs["3"].ZoneActive==True:
        equipementsGicleurs.append(gicleur1.value)
    else:
         equipementsGicleurs.append(-1)
    if gicleurs["4"].ZoneActive==True:
        equipementsGicleurs.append(gicleur1.value)
    else:
         equipementsGicleurs.append(-1)

    return equipementsGicleurs