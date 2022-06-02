from django.shortcuts import render

from app.views import request_get
from .models import CommentaireRepas, OrigineRepas, Repas
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def list(request):
	return render(request, template_name="food/liste.html", context={
        "repass": Repas.objects.filter(approuve=True), 
        "originesRepas": OrigineRepas.objects.order_by("pays")
    })
def show(request, id):
    repas = Repas.objects.get(id=id)
    commentaires = CommentaireRepas.objects.filter(repas=repas).order_by("-date")
    return render(request, template_name="food/show.html", context={
        'repas':repas,
        'commentaires':commentaires
    })

def rate():
    pass
def addComment():
    pass

def getComments():
    pass

@csrf_exempt
def filter(request):
    repass = Repas.filterOnList(request_get(request, "nom"), request_get(request, "composition"), request_get(request, "paysOrigine"), request_get(request, "regionOrigine"));
    return render(request, template_name="load/foods.html", context={"repass":repass})