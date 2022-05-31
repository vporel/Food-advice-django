from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="recommend"),
    path("regles/", views.rules, name="recommend-rules"), # Page  des regles de recommandations
    path("repas/", views.recommendFood, name="recommend-food"), # PAge de recommandation d'un repas
    path("restaurant/", views.recommendRestaurant, name="recommend-restaurant"), # PAge de recommandation d'un restaurant
    path("aliment/", views.recommendAliment, name="recommend-aliment"), # PAge de recommandation d'un restaurant
]