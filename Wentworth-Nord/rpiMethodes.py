import sys, os
from time import sleep
from json import JSONEncoder
import gpiozero
from gpiozero import DigitalInputDevice
from gpiozero import LED, MCP23017

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

def set_relais(nomRelais, statut):
    global gicleur1, gicleur2, gicleur3, gicleur4

    if statut==True:
        print ("statut True")
        if nomRelais =="relais1":
            print ("relais on")
            gicleur1.on()
        if nomRelais =="relais2":
            gicleur2.on()        
        if nomRelais =="relais3":
            gicleur3.on()
        if nomRelais =="relais4":
            gicleur4.on()            
    else:
        if nomRelais =="relais1":
            print ("relais off")
            gicleur1.off()
        if nomRelais =="relais2":
            gicleur2.off()
        if nomRelais =="relais3":
            gicleur3.off()
        if nomRelais =="relais4":
            gicleur4.off()


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

def getValeursGicleurs():
    equipementsGicleurs=list()
    
    equipementsGicleurs.append=gicleur1.value
    equipementsGicleurs.append=gicleur2.value
    equipementsGicleurs.append=gicleur3.value
    equipementsGicleurs.append=gicleur4.value

    return equipementsGicleurs