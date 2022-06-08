import json
from django.http import HttpResponse
from django.shortcuts import render
from app.user_session import getUser

from app.views import request_get
from .models import CommentaireRepas, EvaluationRepas, OrigineRepas, Repas
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def list(request):
    paysOrigines = []
    originesRepas = OrigineRepas.objects.order_by("pays")
    for origineRepas in originesRepas:
        if not paysOrigines.__contains__(origineRepas.pays):
            paysOrigines.append(origineRepas.pays)
    return render(request, template_name="food/liste.html", context={
        "repass": Repas.objects.filter(approuve=True), 
        "originesRepas": originesRepas,
        "paysOrigines": paysOrigines
    })
def show(request, id):
    repas = Repas.objects.get(id=id)
    commentaires = CommentaireRepas.objects.filter(repas=repas).order_by("-date")
    return render(request, template_name="food/show.html", context={
        'repas':repas,
        'commentaires':commentaires
    })

@csrf_exempt
def rate(request, id, rating):
    repas = Repas.objects.get(pk=id)
    try:
        evaluation = EvaluationRepas.objects.get(repas=repas, contributeur=getUser(request.session))
        evaluation.note = rating
    except EvaluationRepas.DoesNotExist:
        evaluation = EvaluationRepas()
        evaluation.repas = repas
        evaluation.contributeur = getUser(request.session)
        evaluation.note = rating
    evaluation.save()
    return HttpResponse(json.dumps({
        "nombreNotes": repas.nombreNotes(),
        "moyenneNotes": repas.moyenneNotes()
    }))

@csrf_exempt
def addComment():
    pass
@csrf_exempt
def getComments():
    pass

@csrf_exempt
def filter(request):
    repass = Repas.filterList(request_get(request, "nom"), request_get(request, "composition"), request_get(request, "paysOrigine"), request_get(request, "regionOrigine"));
    return render(request, template_name="load/foods.html", context={"repass":repass})