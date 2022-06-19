

from datetime import date, datetime, timedelta
from django.db.utils import IntegrityError
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from app.models import momentJourneeText, Repas, RepasConsomme
from app.user_session import getUser
from app.views import request_get
from django.views.decorators.csrf import csrf_exempt

class AddConsumedFoodForm(forms.ModelForm):
    class Meta:
        model=RepasConsomme
        fields= ["date", "momentJournee", "repas", "contributeur"]
        widgets= {
            "date": forms.DateInput(attrs={"type":"date"}),
            "contributeur": forms.HiddenInput
        }

def index(request):
    addConsumedFoodForm = AddConsumedFoodForm(instance=RepasConsomme())
    return render(request, template_name="popup-windows/alimentation-tracking.html", context={
        "addConsumedFoodForm": addConsumedFoodForm
    })

def saveConsumedFood(request, repasConsomme):
    repasConsomme.date = request_get(request, "date")
    repasConsomme.momentJournee = request_get(request, "momentJournee")
    repasConsomme.contributeur = getUser(request.session)
    try:
        repasConsomme.save()
    except IntegrityError:
        return HttpResponse("integrity_error")

    return consumedFoodsList(request)

@csrf_exempt
def addConsumedFood(request, idRepas):
    repasConsomme = RepasConsomme()
    repasConsomme.repas = Repas.objects.get(pk=idRepas)
    return saveConsumedFood(request, repasConsomme)

@csrf_exempt
def updateConsumedFood(request, idRepasConsomme):
    repasConsomme = RepasConsomme.objects.get(pk=idRepasConsomme)
    repasConsomme.repas = Repas.objects.get(pk=request_get(request,"idRepas"))
    return saveConsumedFood(request, repasConsomme)

@csrf_exempt
def deleteConsumedFood(request, idRepasConsomme):
    repasConsomme = RepasConsomme.objects.get(pk=idRepasConsomme)
    repasConsomme.delete()
    return HttpResponse("")

@csrf_exempt
def consumedFoodsList(request):
    repasConsommes = RepasConsomme.objects.filter(contributeur=getUser(request.session)).order_by("-date", "momentJournee")
    return render(request, template_name="load/repas-consommes.html", context={
        "repasConsommesGroupes":RepasConsomme.grouperParDates(repasConsommes)
    })

@csrf_exempt
def getRecommendations(request):
    user = getUser(request.session)
    duree = int(request_get(request, "duree"))
    age = int(user.age())
    sexe = user.sexe
    dateToday = date.today()
    hour = datetime.today().hour
    minDate = None
    minDate = dateToday - timedelta(3 if duree == 1 else 7)
    maxDate = dateToday 
    nextMomentJournee = 1 if hour < 8 else (2 if hour < 14 else 3)
    repasConsommes = RepasConsomme.objects.filter(date__gte=minDate, date__lte=maxDate, contributeur=getUser(request.session))
    repasComptes = [] # Il s'agit des repas dont les aliments sont connus
    for repasConsomme in repasConsommes:
        if repasConsomme.repas.hasRecette() and repasConsomme.repas.recette.aliments.count() > 0:
            repasComptes.append(repasConsomme.repas)
    # S = somme, G = Glucides, L = Lipides, P = Proteines, C = Calories
    SG, SL, SP, SC = 0, 0, 0, 0
    nbreRepas = len(repasComptes)
    for repas in repasComptes:
        SG += repas.tauxGlucides()
        SL += repas.tauxLipides()
        SP += repas.tauxProteines()
        SC += repas.caloriesUnePersonne()
    # M =Moyenne
    MG, ML, MP, MC = round(SG/nbreRepas, 2), round(SL/nbreRepas, 2), round(SP/nbreRepas, 2), round(SC/nbreRepas, 2)
    margeProteines = 5
    if age <= 12:
        glucidesAge, lipidesAge, proteinesAge = 50, 35, 15
        margeGlucides, margeLipides = 10, 5
        margeCalories = 400
        caloriesAgeSexe = 2200 #Kcal
    elif age <= 19:
        glucidesAge, lipidesAge, proteinesAge = 45, 40, 15
        margeGlucides, margeLipides = 8, 7
        margeCalories = 500 if sexe == 1 else 350
        caloriesAgeSexe = 2900 if sexe == 1 else 2500 #Kcal # sexe == 1 : masculin
    else: #adulte
        glucidesAge, lipidesAge, proteinesAge = 47.5, 37.5, 15
        margeGlucides, margeLipides = 6, 6
        margeCalories = 400 if sexe == 1 else 300
        caloriesAgeSexe = 2500 if sexe == 1 else 2100 #Kcal
    elements = {
        "glucides":{
            "moyenne":MG,
            "conseil":glucidesAge,
            "marge": margeGlucides
        },
        "lipides":{
            "moyenne":ML,
            "conseil":lipidesAge,
            "marge": margeLipides
        },
        "proteines":{
            "moyenne":MP,
            "conseil":proteinesAge,
            "marge": margeProteines
        },
        "calories":{
            "moyenne":MC,
            "conseil": caloriesAgeSexe,
            "marge": margeCalories
        }
    }
    elementsEnMoins = []
    elementsEnPlus = []
    for element, values in elements.items():
        if values["moyenne"] < values["conseil"] - values["marge"]:
            elementsEnMoins.append(element)
        if values["moyenne"] > values["conseil"] + values["marge"]:
            elementsEnPlus.append(element)
    elementsEnMoinsRepas = {}
    elementsEnPlusRepas = {}
    for element in elementsEnMoins:
        if element == "glucides":
            composition = "TGD" #taux de glucides décroissant
        elif element == "lipides":
            composition = "TLD"
        elif element == "proteines":
            composition = "TPD"
        else:
            composition = "TCD" #Calories
        elementsEnMoinsRepas[element] = Repas.filterList(composition=composition)[0:4]
    for element in elementsEnPlus:
        if element == "glucides":
            composition = "TGC" #taux de glucides décroissant
        elif element == "lipides":
            composition = "TLC"
        elif element == "proteines":
            composition = "TPC"
        else:
            composition = "TCC" #Calories
        elementsEnPlusRepas[element] = Repas.filterList(composition=composition)[0:4]

    repassAConsommer = []
    return render(request, template_name="load/recommendations-result.html", context={
        "repassAConsommer":repassAConsommer,
        "nbreJours": 3 if duree == 1 else 7,
        "alimentationCorrecte": len(elementsEnMoins) == 0 and len(elementsEnPlus) == 0,
        "elementsEnMoins": ", ".join(elementsEnMoins),
        "elementsEnPlus": ", ".join(elementsEnPlus),
        "elementsEnMoinsRepas": elementsEnMoinsRepas,
        "elementsEnPlusRepas": elementsEnPlusRepas,
        "glucides":elements["glucides"],
        "lipides":elements["lipides"],
        "proteines":elements["proteines"],
        "calories":elements["calories"],
    })
    

@csrf_exempt
def checkConsumedFoodsFilling(request):
    user = getUser(request.session)
    duree = int(request_get(request, "duree"))
    if duree != 1 and duree != 2:
        raise Exception("La durée doit être soit 1 soit 2")
    if int(user.age()) == 0:
        return HttpResponse("age_error")
    if user.sexe == None:
        return HttpResponse("sexe_error")
    dateToday = date.today()
    hour = datetime.today().hour
    minDate = None
    minDate = dateToday - timedelta(3 if duree == 1 else 7)
    maxDate = dateToday 
    nextMomentJournee = 1 if hour < 8 else (2 if hour < 14 else 3)
    repasConsommes = RepasConsomme.objects.filter(date__gte=minDate, date__lte=maxDate, contributeur=getUser(request.session))
    repasConsommesGroupes = RepasConsomme.grouperParDates(repasConsommes)
    # Test du remplissage des repas consomés
    _date = minDate
    while _date <= dateToday:
        _momentJournee = 1
        if not repasConsommesGroupes.__contains__(_date):
            return HttpResponse("fill_error:"+str(_date))
        while _momentJournee <= 3:
            momentJourneeRempli = False
            for repasConsomme in repasConsommesGroupes[_date]:
                if(repasConsomme.momentJournee == _momentJournee):
                    momentJourneeRempli = True 
                    break
            if not momentJourneeRempli and (_date != maxDate or _momentJournee < nextMomentJournee):
                return HttpResponse("fill_error:"+str(_date)+":"+momentJourneeText(_momentJournee))
            _momentJournee += 1
        _date += timedelta(1)
    return HttpResponse("")
    
