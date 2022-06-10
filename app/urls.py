from django.contrib import admin
from django.urls import path, include
from . import views, views_foods, views_aliments, views_restaurants, views_account, views_extra, views_conversations, views_recommendations

urlpatterns = [
    #Route page d'accueil
    path("", views.index, name="home"),

    path("contributeur/<nomUtilisateur>", views_account.userAccount, name="contributor"), 
    path("professionnels", views_account.professionalsList, name="professionals-list"), 
    path("filtre-professionnels", views_account.professionalsFilter, name="professionals-filter"),

    path('mon-compte/', include([
        path("", views_account.myaccount, name="myaccount"), #Page de gestion du compte utilisateur
        path("connexion/", views_account.login, name="login"), #Page de connexion
        path("inscription/", views_account.signin, name="signin"), # Page d'enregistrement
        path("deconnexion/", views_account.logout, name="logout"), 
    ])),

    #Routes pour les conversations
    path("conversations", views_conversations.conversations, name="conversations"), 
    path("nbre-messages-non-lus", views_conversations.unreadMessagesCount, name="unread-messages-count"),
    path("chat", views_conversations.chat, name="chat"),
    path("conversation/", include([
        path("recherche/<int:idProfessionnel>", views_conversations.search, name="search-conversation"),
        path("nouvelle/<int:idProfessionnel>", views_conversations.new, name="new-conversation"),
        path("<int:id>/charger/", views_conversations.load, name="load-conversation"), # Renvoie juste le code qui présente la conversation
        path("<int:id>/envoie-message/", views_conversations.sendMessage, name="send-message"),
        path("<int:id>/supprimer/",  views_conversations.delete, name="delete-conversation"),
        path("<int:id>/messages/", views_conversations.messages, name="conversation-messages"),
        path("<int:id>/messages-non-lus/", views_conversations.unreadMessages, name="conversation-unread-messages"),
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
    path("recommander/", include([
        path("", views_recommendations.index, name="recommend"),
        path("regles/", views_recommendations.rules, name="recommend-rules"), # Page  des regles de recommandations
        path("repas/", views_recommendations.recommendFood, name="recommend-food"), # PAge de recommandation d'un repas
        path("repas/<int:id>/recette", views_recommendations.recommendFoodRecipe, name="recommend-food-recipe"), # PAge de recommandation de la recette d'un repas
        path("repas/<int:id>/recette/aliment", views_recommendations.recommendFoodRecipeAliment, name="recommend-food-recipe-aliment"), # PAge de recommandation de la recette d'un repas
        path("restaurant/", views_recommendations.recommendRestaurant, name="recommend-restaurant"), # PAge de recommandation d'un restaurant
        path("aliment/", views_recommendations.recommendAliment, name="recommend-aliment"), # PAge de recommandation d'un restaurant
    ])),
    path("help/", views_extra.help, name="help",), # Page d'aide
    path("souscription-newsletter/",  views_extra.subscribeToNewsletter, name="subscribe-to-newsletter") #Page d'abonnement à la newsletter
]