import os
from .models import *

### Renvoie la liste de toutes les maladies
def pathologyChoices():

    temp = Pathology.query.with_entities(Pathology.id, Pathology.name, Pathology.other_name).all()
    other_name_temp = []

    for x in temp:
        if x[2]:
            array = x[2].split(",")

            for i in range(len(array)):
                if array[i] is not None:
                    other_name_temp.append((x[0], array[i].strip()))

    choices = [(x[0], x[1]) for x in temp] + other_name_temp

    i = 0
    l = len(choices)
    while (i < l and choices[i]):
        if choices[i][1] == '':
            del choices[i]
            l -= 1
        else:
            i += 1

    return choices

#renvoie la liste de tous les users
def userChoices():

    temp = User.query.with_entities(User.id, User.forename).all()
    choices = [(x[0], x[1]) for x in temp]
    return choices


#renvoie la liste des classes
def allClasses():
    temp = TreatementClass.query.with_entities(Classes.id, Classes.name).all()
    choices = [( x[0], x[1] ) for x in temp]
    return choices

#renvoie la liste des classes id
def allClassesId():
    temp = TreatementClass.query.with_entities(Classes.id, Classes.name).all()
    choices = [(x[0]) for x in temp]
    return choices

#Renvoie liste molecules selon les classes
def allMoleculeFilterByClass(id):
    temp = Classes_families.query.with_entities(Classes_families.molecule_id).filter_by(class_id= id)
    choices = [(x[0]) for x in temp]
    return choices

#Renvoie liste molecules selon les classes
def allMoleculeFilterByClassName(id):
    temp = Molecule.query.with_entities(Molecule.name).filter_by(id = id)
    choices = [(x[0]) for x in temp]
    return choices