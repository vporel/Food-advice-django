from .models import Contributeur

"""
    Objet du type HttpRequest
"""
def isUserConnected(session):
    return session.__contains__("user_id")

def connectUser(session, id):
    return session.__setitem__("user_id", id)

def disconnectUser(session):
    session.__delitem__("user_id")

def getUser(session):
    if isUserConnected(session):
        return Contributeur.objects.get(id=session["user_id"])
    else:
        return None