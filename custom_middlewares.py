"""
    Code qui va vérifier certaines routes lors de l'exécution d'une requete
"""
import re

from django.shortcuts import redirect
from app.user_session import isUserConnected


def authentication_middleware(response_function):
    def middleware(request):
        response = response_function(request)
        regexList = ["^/mon-compte(?!/connexion|/inscription|/deconnexion)", "^/recommender"]
        onSecurePath = False
        for regex in regexList:
            if re.search(regex, request.path):
                onSecurePath = True
                break
        if onSecurePath and not isUserConnected(request.session):
            return redirect("login")
        return response
    
    return middleware