from email import message
from django import forms
from django.shortcuts import redirect, render
from app.models import Contributeur

from app.user_session import connectUser, getUser, isUserConnected
from app.views import request_get

class LoginForm(forms.ModelForm):
    class Meta:
        model=Contributeur
        fields = ["nomUtilisateur", "motDePasse"]
        widgets = {
            "motDePasse": forms.PasswordInput
        }
class SigninForm(forms.ModelForm):
    class Meta:
        model=Contributeur
        fields = ["nom", "nomUtilisateur", "motDePasse","email", "professionnelSante"]
        widgets = {
            "motDePasse": forms.PasswordInput
        }
    confirmerMotDePasse = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

# Create your views here.

def myaccount(request):
    return render(request, template_name="account/user-account.html", context={
			"user" : getUser(request.session)
    })

def userAccount(request, nomUtilisateur):
	user = Contributeur.objects.get(nomUtilisateur=nomUtilisateur)
	return render(request, template_name="account/user-account.php", context={"user":user, nomUtilisateur:"nomUtilisateur"})

def login(request):
    if not isUserConnected(request.session):
        contributeur = Contributeur()
        form = LoginForm(instance=contributeur)
        msg = ""
        if request.method == "POST":
            form = LoginForm(request.POST, instance=contributeur)
            if form.is_valid():
                contributeur = form.save(commit=False)
                try:
                    contributeurExistant = Contributeur.objects.get(nomUtilisateur=contributeur.nomUtilisateur)
                    if contributeurExistant.motDePasse == contributeur.motDePasse:
                        connectUser(request.session, contributeurExistant.id)
                        """urlBeforeRedirection = Security::getURLBeforeRedirection()
                        if(urlBeforeRedirection != null)
                            this->redirect(urlBeforeRedirection)
                        else
                        """
                        return redirect("myaccount")
                    else:
                        msg = "Mot de passe incorrect"
                except Contributeur.DoesNotExist:
                    msg = "Utilisateur non reconnu"
        return render(request, template_name="account/login.html", context={"form":form, "msg":msg})
    else:
        return redirect("myaccount")

def logout():
    pass
def signin(request):
    if isUserConnected(request.session):
        redirect("myaccount")
    contributeur = Contributeur()
    form = SigninForm(instance=contributeur)
    msg = ""
    if request.method == "POST":
        form = SigninForm(request.POST, instance=contributeur)
        if form.is_valid():
            contributeur = form.save(commit=False)
            try:
                contributeurExistant = Contributeur.objects.get(nomUtilisateur=contributeur.nomUtilisateur)
                msg = "Ce nom d'utilisateur est déjà pris"
            except Contributeur.DoesNotExist:
                if form.cleaned_data["confirmerMotDePasse"] == form.cleaned_data["motDePasse"]:
                    contributeur.save()
                    connectUser(request.session, contributeur.id)
                    redirect("myaccount")
                else:
                    msg = "Les mots de passe ne sont pas identiques"
    return render(request, template_name="account/signin.html", context={"form":form, "msg":msg})

def professionalsList(request):
    nom = request_get(request, "nom")
    if nom != None:
        professionals = Contributeur.professionnels.filter(nom__contains=nom)
    else:
        professionals = Contributeur.professionnels
    return render(request,template_name="account/professionals-list.html", context={
        "professionals":professionals,
        "nom": nom
    })

"""
    Le paramètre messagesBox peut être passé dans la requete
    Ce paramètre indiquera que le filtre ets demandé pour la boite des messages et donc le template retourné sera différent
"""
def professionalsFilter(request, nom):
    messagesBox = request_get(request, "messagesBox")
    nom = request_get(request, "nom")
    if nom != None:
        professionals = Contributeur.professionnels.filter(nom__contains=nom)
    else:
        professionals = Contributeur.professionnels
    if messagesBox != None and messagesBox == True: #Si le filtre est demandé pour la boite des messages
        return render(request, template_name="load/professionals-for-messages-box.php", context={"professionals":professionals});
    return render(request, template_name="load/professionals.php", context={"professionals":professionals});