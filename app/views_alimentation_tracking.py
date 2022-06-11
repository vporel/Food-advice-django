

from django.db.utils import IntegrityError
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from app.models import Repas, RepasConsomme
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
    repasConsommesGroupes = {}
    for repasConsomme in repasConsommes:
        date = repasConsomme.date
        if not repasConsommesGroupes.__contains__(date):
            repasConsommesGroupes[date] = []
        repasConsommesGroupes[date].append(repasConsomme)
    return render(request, template_name="load/repas-consommes.html", context={
        "repasConsommesGroupes":repasConsommesGroupes
    })

@csrf_exempt
def getRecommendations(request):
    user = getUser(request.session)
    duree = int(request_get(request, "duree"))
    age = int(user.age())
    if duree != 1 and duree != 2:
        raise Exception("La durée doit être soit 1 soit 2")
    if age == 0:
        return HttpResponse("age_error");
    if age <= 12:
        pass
    repassAConsommer = []
    return render(request, template_name="load/repass-a-consommer.html", context={
        "repassAConsommer":repassAConsommer
    })
    





