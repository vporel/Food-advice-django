

from django.http import HttpResponse
from django.shortcuts import render
from app.models import Repas, RepasConsomme
from app.user_session import getUser
from app.views import request_get
from django.views.decorators.csrf import csrf_exempt


def saveConsumedFood(request, repasConsomme):
    repasConsomme.date = request_get(request, "date")
    repasConsomme.momentJournee = request_get(request, "momentJournee")
    repasConsomme.contributeur = getUser(request.session)
    repasConsomme.save()

    return render(request, template_name="load/repass-consommes.html", context={
        "repasConsommes":[repasConsomme] #Tableau contenant le repas qui vient d'être enregistré
    })

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
    repasConsommes = RepasConsomme.objects.filter(contributeur=getUser(request.session)).order_by("-date")
    return render(request, template_name="load/repass-consommes.html", context={
        "repasConsommes":repasConsommes
    })

@csrf_exempt
def getRecommendations(request):
    user = getUser(request.session)
    duree = request_get(request, "duree")
    age = user.age()
    if duree != 1 and duree != 2:
        raise Exception("La durée doit être soit 1 soit 2")
    if age == 0:
        raise Exception("Recommandations impossible si l'age n'est pas renseignée")
    if age <= 12:
        pass
    repassAConsommer = []
    return render(request, template_name="load/repass-a-consommer.html", context={
        "repassAConsommer":repassAConsommer
    })
    





