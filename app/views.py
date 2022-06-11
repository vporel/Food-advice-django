from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.models import Aliment, Repas, Restaurant
from app.user_session import isUserConnected

"""
    Retourne le paramètre 'key' de la requete en cherchant dans POST et GET
"""
def request_get(request:HttpRequest, key:str):
    return  request.POST.get(key) if request.method == "POST" else request.GET.get(key)



# Create your views here.
def index(request):
    maxElements = 8
    repass = Repas.objects.filter(approuve=True).order_by("dateDerniereModification")[0:maxElements]
    aliments = Aliment.objects.filter(approuve=True).order_by("dateDerniereModification")[0:maxElements]
    restaurants = Restaurant.objects.filter(approuve=True).order_by("dateDerniereModification")[0:maxElements]
    return render(request, template_name="home.html", context={
        "repass":repass,
        "aliments":aliments,
        "restaurants":restaurants
    })
 
