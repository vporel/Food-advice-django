
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from app.models import Contributeur, Conversation, Message
from app.user_session import getUser
from django.db.models import Q


def sendMessage(request, id):
    conversation = Conversation.objects.get(pk=id)
    message = Message(conversation)
    message.message = request.POST.get("message")
    message.expediteur = getUser(request.session)
    message.save()
    conversation.dateDernierMessage = message.date
    conversation.visiblePourContributeur = True
    conversation.visiblePourProfessionnel = True
    conversation.save()
    return render(request, template_name="load/messages.html", context={"messages":message})

def new(request, idProfessionnel):
    conversation = Conversation()
    conversation.contributeur = getUser(request.session)
    conversation.professionnel(Contributeur.objects.get(pk=idProfessionnel))
    conversation.save()
    return  JsonResponse({"idConversation":conversation.id})


def messages(request, id):
    conversation = Conversation.objects.get(pk=id)
    messages = conversation.message_set.all()
    for message in messages:
        if message.objetExpediteur().id != getUser(request.session).id:
            message.lu = True
            message.save()
    return render(request, template_name="load/messages.html", context={
        "messages": messages # Les messages seront données dans l'ordre de leur enregistrement dans la base
    })

def delete(request, id):
    conversation = Conversation.objects.get(pk=id)
    conversation.supprimer(getUser(request.session))
    conversation.save()
    return HttpResponse("")

"""
    Rechercher tours les conversations dans lesquelles le contributeur connecté intervient
    On retourne uniquement celles avec la visibilité activée
    En effet, si un contributeur supprime une coversation, elle n'est pas enlevée de la base de données
    mais la propriété visiblePourContributeur passe à False
    Pareil pour un professionnel
"""
def conversations(request):
    conversations = Conversation.objects.filter(Q(contributeur=getUser(request.session), visiblePourContributeur=True) | Q(professionnel=getUser(request.session), visiblePourProfessionnel=True)).order_by("-dateDernierMessage") 
    return render(request, template_name="load/conversations.html", context={
        "conversations":conversations   
    })

"""
    Rechercher la conversation dans entre le contributeur connecté et le professionnel en paramètre
"""
def search(request, idProfessionnel):
    conversation = Conversation.objects.get(contributeur=getUser(request.session), professionnel=Contributeur.objects.get(pk=idProfessionnel))
    return JsonResponse({"idConversation":conversation.id if conversation != None else 0})

"""
    Charger la conversation à l'id passé en paramètre
"""
def load(request, id):
    conversation = Conversation.objects.get(pk=id)
    return render(request, template_name="load/conversations.html", context={
        "conversations":[conversation]
    })

"""
    Recupérer le nombre total de messages non lus par le contributeur connecté.
    Toutes les conversations confondues
"""
def unreadMessagesCount(request):
    return HttpResponse(getUser(request.session).nbreMessagesNonLus())


def unreadMessages(request, id):
    conversation = Conversation.objects.get(pk=id) 
    messages = conversation.messagesNonLus(getUser(request.session))
    for message in messages:
        if message.objetExpediteur().id != getUser(request.session).id:
            message.lu = True
            message.save()
    return render(request, template_name="load/messages.html", context={
        "messages":messages 
    })
