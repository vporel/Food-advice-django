
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from app.models import Contributeur, Conversation, Message
from app.user_session import getUser
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


def chat(request):
    return render(request, template_name="chat.html")

@csrf_exempt
def sendMessage(request, id):
    conversation = Conversation.objects.get(pk=id)
    message = Message()
    message.conversation = conversation
    message.message = request.POST.get("message")
    message.expediteur = getUser(request.session)
    message.save()
    conversation.dateDernierMessage = message.date
    conversation.visiblePourContributeur = True
    conversation.visiblePourProfessionnel = True
    conversation.save()
    return render(request, template_name="load/messages.html", context={"messages":[message]})

@csrf_exempt
def new(request, idProfessionnel):
    conversation = Conversation()
    conversation.contributeur = getUser(request.session)
    conversation.professionnel = Contributeur.objects.get(pk=idProfessionnel)
    conversation.save()
    return  HttpResponse(json.dumps({"idConversation":conversation.id}))


@csrf_exempt
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

@csrf_exempt
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
@csrf_exempt
def search(request, idProfessionnel):
    try:
        conversation = Conversation.objects.get(contributeur=getUser(request.session), professionnel=Contributeur.objects.get(pk=idProfessionnel))
        idConversation = conversation.id
    except Conversation.DoesNotExist:
        idConversation = 0
    return HttpResponse(json.dumps({"idConversation":idConversation}))

"""
    Charger la conversation à l'id passé en paramètre
"""
@csrf_exempt
def load(request, id):
    conversation = Conversation.objects.get(pk=id)
    return render(request, template_name="load/conversations.html", context={
        "conversations":[conversation]
    })

"""
    Recupérer le nombre total de messages non lus par le contributeur connecté.
    Toutes les conversations confondues
"""
@csrf_exempt
def unreadMessagesCount(request):
    return HttpResponse(getUser(request.session).nbreMessagesNonLus())


@csrf_exempt
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
