from django.shortcuts import render

from app.models import Aliment, Repas, Restaurant


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