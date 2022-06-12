import json
from re import template
from django.http import HttpResponse
from django.shortcuts import render
from app.user_session import getUser

from app.views import request_get
from .models import CommentaireRestaurant, EvaluationRestaurant, Restaurant
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# Create your views here.
def list(request):
    nom = request_get(request, "nom")
    if nom != None:
        restaurants = Restaurant.objects.filter(approuve=True, nom__contains=nom)
    else:
        restaurants = Restaurant.objects.filter(approuve=True)
    
    return render(request, template_name="restaurant/liste.html", context={
        "restaurants": restaurants, 
        "nom":nom if nom != None else "" 
    })
def show(request, id):
    restaurant = Restaurant.objects.get(id=id)
    commentaires = CommentaireRestaurant.objects.filter(restaurant=restaurant).order_by("-date")
    return render(request, template_name="restaurant/show.html", context={
        'restaurant':restaurant,
        'commentaires':commentaires,
        'autresRestaurant':Restaurant.objects.filter(~Q(pk=id), Q(approuve=True) | Q(~Q(contributeur=None), contributeur=getUser(request.session)))[0:6]
    })

@csrf_exempt
def rate(request, id, rating):
    restaurant = Restaurant.objects.get(pk=id)
    try:
        evaluation = EvaluationRestaurant.objects.get(restaurant=restaurant, contributeur=getUser(request.session))
        evaluation.note = rating
    except EvaluationRestaurant.DoesNotExist:
        evaluation = EvaluationRestaurant()
        evaluation.restaurant = restaurant
        evaluation.contributeur = getUser(request.session)
        evaluation.note = rating
    evaluation.save()
    return HttpResponse(json.dumps({
        "nombreNotes": restaurant.nombreNotes(),
        "moyenneNotes": restaurant.moyenneNotes()
    }))

@csrf_exempt#pour appeler la méthode en ajax
def addComment(request, id):
    commentaire = CommentaireRestaurant()
    commentaire.restaurant = Restaurant.objects.get(pk=id)
    commentaire.texte = request_get(request, "comment")
    commentaire.contributeur = getUser(request.session)
    commentaire.save()
    return render(request, template_name="load/comments.html", context={"commentaires":[commentaire]});      

@csrf_exempt
def getComments(request):
    restaurant = Restaurant.objects.get(pk=id)
    commentaires = CommentaireRestaurant.objects.filter(restaurant=restaurant).order_by("-date") 
    return render(request, template_name="load/comments.html", context={"commentaires":commentaires})

@csrf_exempt
def filter(request):
    restaurants = Restaurant.filterList(request_get(request, "nom"), request_get(request, "nomRepas"))
    return render(request, template_name="load/restaurants.html", context={"restaurants":restaurants})