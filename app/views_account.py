
from django import forms
from django.shortcuts import redirect, render
from app.models import Contributeur
from django.views.decorators.csrf import csrf_exempt

from app.user_session import connectUser, disconnectUser, getUser, isUserConnected
from app.views import request_get
from functions import hashPassword

class LoginForm(forms.Form):
    nomUtilisateur = forms.CharField(label="Nom d'utilisateur")
    motDePasse = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    
class SigninForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model=Contributeur
        fields = ["nom", "nomUtilisateur", "professionnelSante","motDePasse"]
        widgets = {
            "motDePasse": forms.PasswordInput,
        },
        error_messages = {
            "nomUtilisateur":{
                "unique":"Un autre contributeur a déjà ce nom d'utilisateur"
            }
        }
    confirmerMotDePasse = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["confirmerMotDePasse"] != cleaned_data["motDePasse"]:
            self.add_error("confirmerMotDePasse", "Les mots de passe ne sont pas identiques")

# Create your views here.

def myaccount(request):
    return render(request, template_name="account/user-account.html", context={
			"user" : getUser(request.session)
    })

def userAccount(request, nomUtilisateur):
	user = Contributeur.objects.get(nomUtilisateur=nomUtilisateur)
	return render(request, template_name="account/user-account.html", context={"user":user, nomUtilisateur:"nomUtilisateur"})

def login(request):
    if not isUserConnected(request.session):
        form = LoginForm()
        msg = ""
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                try:
                    contributeurExistant = Contributeur.objects.get(nomUtilisateur=form.cleaned_data["nomUtilisateur"])
                    if contributeurExistant.motDePasse == hashPassword(form.cleaned_data["motDePasse"]):
                        connectUser(request.session, contributeurExistant.id)
                        """urlBeforeRedirection = Security::getURLBeforeRedirection()
                        if(urlBeforeRedirection != null)
                            this->redirect(urlBeforeRedirection)
                        else
                        """
                        return redirect("myaccount")
                    else:
                        form.add_error("motDePasse", "Mot de passe incorrect")
                except Contributeur.DoesNotExist:
                    form.add_error("nomUtilisateur", "Utilisateur non reconnu")
                    print("ssdqsdqsdqsd")
        return render(request, template_name="account/login.html", context={"form":form})
    else:
        return redirect("myaccount")

def logout(request):
    disconnectUser(request.session)
    return redirect("login")
    

def signin(request):
    if isUserConnected(request.session):
        return redirect("myaccount")
    contributeur = Contributeur()
    form = SigninForm(instance=contributeur)
    msg = ""
    if request.method == "POST":
        form = SigninForm(request.POST, instance=contributeur)
        if form.is_valid():
            contributeur = form.save(commit=False)
            contributeur.motDePasse = hashPassword(contributeur.motDePasse)
            contributeur.save()
            connectUser(request.session, contributeur.id)
            return redirect("myaccount")
    return render(request, template_name="account/signin.html", context={"form":form, "msg":msg})

def professionalsList(request):
    nom = request_get(request, "nom")
    if nom != None:
        professionnels = Contributeur.objects.filter(professionnelSante=True, nom__contains=nom)
    else:
        professionnels = Contributeur.professionnels
    return render(request,template_name="account/professionals-list.html", context={
        "professionnels":professionnels,
        "nom": nom
    })

"""
    Le paramètre messagesBox peut être passé dans la requete
    Ce paramètre indiquera que le filtre ets demandé pour la boite des messages et donc le template retourné sera différent
"""

@csrf_exempt
def professionalsFilter(request):
    messagesBox = request_get(request, "messagesBox")
    nom = request_get(request, "nom")
    if nom != None:
        professionnels = Contributeur.objects.filter(professionnelSante=True, nom__contains=nom)
    else:
        professionnels = Contributeur.professionnels
    if messagesBox != None and messagesBox: #Si le filtre est demandé pour la boite des messages
        return render(request, template_name="load/professionals-for-messages-box.html", context={"professionnels":professionnels})
    return render(request, template_name="load/professionals.html", context={"professionnels":professionnels})