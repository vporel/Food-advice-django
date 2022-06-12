from django.shortcuts import render

from app.models import Aliment, CommentaireAliment
from django.db.models import Q

from app.user_session import getUser

# Create your views here.

def list(request):
    return render(request, template_name="aliment/liste.html", context={
        "aliments": Aliment.objects.filter(approuve=True), 
    })
def show(request, id):#présentation d'un aliment
    aliment = Aliment.objects.get(id=id)
    commentaires = CommentaireAliment.objects.filter(aliment=aliment).order_by("-date")
    return render(request, template_name="aliment/show.html", context={
        'aliment':aliment,
        'commentaires':commentaires,
        'autresAliments':Aliment.objects.filter(~Q(pk=id), Q(approuve=True) | Q(contributeur=getUser(request.session)), type=aliment.type)[0:6]
    })
def addComment():
    pass

def getComments():
    pass

def filter():
    pass