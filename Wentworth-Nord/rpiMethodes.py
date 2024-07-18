import sys, os
from time import sleep
from json import JSONEncoder
import gpiozero
from gpiozero import LED
from gpiozero import LED


relais0 = gpiozero.OutputDevice(0, active_high=False, initial_value=False)
relais1=  gpiozero.OutputDevice(4, active_high=False, initial_value=False)
relais2=relais0
relais3=relais0
relais4=relais0


def getPinStatut(pinNo):
    valeur = LED(pinNo)
    return valeur.is_active


def get_relais(nomRelais):
    global relais1, relais2, relais3, relais4

    valeur=False

    if nomRelais=="relais1":
       valeur= relais1.value
    if nomRelais=="relais2":
        valeur= relais2.value
    if nomRelais=="relais3":
        valeur= relais3.value            
    if nomRelais=="relais4":
        valeur= relais4.value
    
    return valeur

def set_relais(nomRelais, statut):
    global relais1, relais2, relais3, relais4

    if statut==True:
        print ("statut True")
        if nomRelais =="relais1":
            print ("relais on")
            relais1.on()
        if nomRelais =="relais2":
            relais2.on()        
        if nomRelais =="relais3":
            relais3.on()
        if nomRelais =="relais4":
            relais4.on()            
    else:
        if nomRelais =="relais1":
            print ("relais off")
            relais1.off()
        if nomRelais =="relais2":
            relais2.off()
        if nomRelais =="relais3":
            relais3.off()
        if nomRelais =="relais4":
            relais4.off()


    PanneElectrique: float = 0.0

def getAlarmeDetecteur(detecteurAlarme, fumeePin,mouvementPin, eauElectriquePin,eauTraitementPin,panneElectriquePin):
    detecteurAlarme.Prop=-1.0
    detecteurAlarme.Co=-1.0
    detecteurAlarme.Fumee =  getPinStatut(fumeePin)
    detecteurAlarme.Mouvement=  getPinStatut(mouvementPin)
    detecteurAlarme.EauTraitement = getPinStatut(eauTraitementPin)
    detecteurAlarme.EauElectrique = getPinStatut(eauElectriquePin)
    detecteurAlarme.PanneElectrique = getPinStatut(panneElectriquePin)

    return detecteurAlarme

def getArrosageDetecteur(gicleursStatut):
    gicleursStatut["1"].statut = get_relais("relais1")
    gicleursStatut["2"].statut=False
    gicleursStatut["3"].statut=False
    gicleursStatut["4"].statut=False

    return gicleursStatut