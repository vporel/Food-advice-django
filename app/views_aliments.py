from django.shortcuts import render

from app.models import Aliment, CommentaireAliment
from django.db.models import Q

from app.user_session import getUser
from django.views.decorators.csrf import csrf_exempt
from app.views import request_get

# Create your views here.

def list(request):
    nom = request_get(request, "nom")
    if nom != None:
        aliments = Aliment.objects.filter(approuve=True, nom__contains=nom)
    else:
        aliments = Aliment.objects.filter(approuve=True)
    return render(request, template_name="aliment/liste.html", context={
        "aliments": aliments, 
        "nom":nom if nom != None else "" 
    })
def show(request, id):#présentation d'un aliment
    aliment = Aliment.objects.get(id=id)
    commentaires = CommentaireAliment.objects.filter(aliment=aliment).order_by("-date")
    return render(request, template_name="aliment/show.html", context={
        'aliment':aliment,
        'commentaires':commentaires,
        'autresAliments':Aliment.objects.filter(~Q(pk=id), Q(approuve=True) | Q(contributeur=getUser(request.session)), type=aliment.type)[0:6]
    })
@csrf_exempt #pour appeler la méthode en ajax
def addComment(request, id):
    commentaire = CommentaireAliment()
    commentaire.aliment = Aliment.objects.get(pk=id)
    commentaire.texte = request_get(request, "comment")
    commentaire.contributeur = getUser(request.session)
    commentaire.save()
    return render(request, template_name="load/comments.html", context={"commentaires":[commentaire]});      

@csrf_exempt
def getComments(request):
    aliment = Aliment.objects.get(pk=id)
    commentaires = CommentaireAliment.objects.filter(aliment=aliment).order_by("-date") 
    return render(request, template_name="load/comments.html", context={"commentaires":commentaires})

@csrf_exempt
def filter(request):
    aliments = Aliment.filterList(request_get(request, "nom"), request_get(request, "composition"));
    return render(request, template_name="load/aliments.html", context={"aliments":aliments})