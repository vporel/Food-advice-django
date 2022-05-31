from django import forms
from django.shortcuts import redirect, render
from app.models import Contributeur

from app.user_session import connectUser, getUser, isUserConnected

class LoginForm(forms.ModelForm):
    class Meta:
        model=Contributeur
        fields = ["nomUtilisateur", "motDePasse"]
        labels = {
            "nomUtilisateur": "Nom d'utilisateur",
            "motDePasse": "Mot de passe"
        }
        widgets = {
            "motDePasse": forms.PasswordInput
        }
class SigninForm(forms.ModelForm):
    class Meta:
        model=Contributeur
        fields = ["nom", "nomUtilisateur", "motDePasse","email"]
        labels = {
            "nom": "Nom",
            "nomUtilisateur": "Nom d'utilisateur",
            "motDePasse": "Mot de passe",
            "email": "Adresse email"
        }
        widgets = {
            "motDePasse": forms.PasswordInput
        }
    confirmerMotDePasse = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

# Create your views here.

def myaccount(request):
    return render(request, template_name="account/user-account.html", context={
			"user" : getUser(request.session)
    })

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
