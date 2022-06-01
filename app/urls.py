from django.contrib import admin
from django.urls import path, include
from . import views, views_foods, views_aliments, views_restaurants, views_account, views_extra

urlpatterns = [
    #Route page d'accueil
    path("", views.index, name="home"),

    path('mon-compte/', include([
        path("", views_account.myaccount, name="myaccount"), #Page de gestion du compte utilisateur
        path("connexion/", views_account.login, name="login"), #Page de connexion
        path("inscription/", views_account.signin, name="signin"), # Page d'enregistrement
        path("deconnexion/", views_account.logout, name="logout"), 
    ])),

    path('repas/', include([
        path("" , views_foods.list, name="foods-list"), 
        path("<int:id>", views_foods.show, name="show-food"),
        path("<int:id>/noter/<rating>", views_foods.rate, name="rate-food"),
        path("<int:id>/commenter", views_foods.addComment, name="food-add-comment"),
        path("<int:id>/commentaires", views_foods.getComments, name="food-comments"),
        path("filtre", views_foods.filter, name="foods-filter")
    ])),
    path('aliments/', include([
        path("" , views_aliments.list, name="aliments-list"), 
        path("<int:id>", views_aliments.show, name="show-aliment"),
        path("<int:id>/commenter", views_aliments.addComment, name="aliment-add-comment"),
        path("<int:id>/commentaires", views_aliments.getComments, name="aliment-comments"),
        path("filtre", views_aliments.filter, name="aliments-filter")
    ])),
    path('restaurants/', include([
        path("" , views_restaurants.list, name="restaurants-list"), 
        path("<int:id>", views_restaurants.show, name="show-restaurant"),
        path("<int:id>/noter/<rating>", views_restaurants.rate, name="rate-restaurant"),
        path("<int:id>/commenter", views_restaurants.addComment, name="restaurant-add-comment"),
        path("<int:id>/commentaires", views_restaurants.getComments, name="restaurant-comments"),
        path("filtre", views_restaurants.filter, name="restaurants-filter")
    ])),
    path("help/", views_extra.help, name="help",), # Page d'aide
    path("souscription-newsletter/",  views_extra.subscribeToNewsletter, name="subscribe-to-newsletter") #Page d'abonnement à la newsletter
]