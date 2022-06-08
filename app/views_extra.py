from django.shortcuts import redirect, render
from app.models import AdresseNewsletter

from app.views import request_get

# Create your views here.

def help(request):
	return render(request, template_name="extra/help.html");

def subscribeToNewsletter(request):
    email = request_get(request,"newsletter-email")
    if email != None:
        try:
            AdresseNewsletter.objects.get(email=email)
            alreadySubscriber = True
        except AdresseNewsletter.DoesNotExist:
            adresse = AdresseNewsletter()
            adresse.email = email
            adresse.save()
            alreadySubscriber = False
        return render(request, template_name="extra/newsletter-subscription.html", context={
            "alreadySubscriber":alreadySubscriber, "email":email
        })
    else:
        return redirect("home");