

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
    if duree != 1 and duree != 2:
        raise Exception("La durée doit être soit 1 soit 2")
    if age == 0:
        return HttpResponse("age_error")
    dateToday = date.today()
    hour = datetime.today().hour
    minDate = None
    minDate = dateToday - timedelta(3 if duree == 1 else 7)
    maxDate = dateToday 
    nextMomentJournee = 1 if hour < 8 else (2 if hour < 14 else 3)
    repasConsommes = RepasConsomme.objects.filter(date__gte=minDate, date__lte=maxDate)
    
    if age <= 12:
        pass
    repassAConsommer = []
    return render(request, template_name="load/repass-a-consommer.html", context={
        "repassAConsommer":repassAConsommer
    })
    

@csrf_exempt
def checkConsumedFoodsFilling(request):
    user = getUser(request.session)
    duree = int(request_get(request, "duree"))
    age = int(user.age())
    if duree != 1 and duree != 2:
        raise Exception("La durée doit être soit 1 soit 2")
    if age == 0:
        return HttpResponse("age_error")
    dateToday = date.today()
    hour = datetime.today().hour
    minDate = None
    minDate = dateToday - timedelta(3 if duree == 1 else 7)
    maxDate = dateToday 
    nextMomentJournee = 1 if hour < 8 else (2 if hour < 14 else 3)
    repasConsommes = RepasConsomme.objects.filter(date__gte=minDate, date__lte=maxDate)
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
                    break;
            if not momentJourneeRempli and _date != maxDate and _momentJournee < nextMomentJournee:
                return HttpResponse("fill_error:"+str(_date)+":"+momentJourneeText(_momentJournee))
            _momentJournee += 1
        _date += timedelta(1)
    return HttpResponse("")
    
