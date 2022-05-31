from django.shortcuts import render
from .models import CommentaireRepas, Repas
# Create your views here.

def list():
    pass

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

def filter():
    pass