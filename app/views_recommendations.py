from re import A
from django import forms
from django.shortcuts import redirect, render

from app.models import Aliment, AlimentRecette, Recette, Repas, Restaurant
from app.user_session import getUser
from app.views import request_get

class RecommendFoodForm(forms.ModelForm):
    class Meta:
        model = Repas
        fields = ["nom", "image", "description", "momentJournee"]

class RecommendFoodRecipeForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ["repas", "nombrePersonnes", "tempsPreparation","tempsCuisson", "detailPreparation"]
        widgets = {
            "repas":forms.HiddenInput
        }

class RecommendFoodRecipeAlimentForm(forms.ModelForm):
    class Meta:
        model = AlimentRecette
        fields = ["recette", "aliment", "quantite"]
        widgets = {
            "recette":forms.HiddenInput
        }
class RecommendAlimentForm(forms.ModelForm):
    class Meta:
        model = Aliment
        fields = ["nom", "image", "uniteComptage", "masseUnite", "tauxGlucides", "tauxLipides", "tauxProteines", "type", "description","detailApports", "detailRisques"]
        
class RecommendRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["nom", "image", "description", "adresse"]

# Create your views here.
def index(request):
    return render(request, template_name="recommendation/index.html")

def recommendFood(request):
    form = RecommendFoodForm(instance=Repas())
    if request.method == "POST":
        form = RecommendFoodForm(request.POST, request.FILES, instance=Repas())
        if form.is_valid():
            repas = form.save(commit=False)
            repas.contributeur = getUser(request.session)
            repas.save()
            return redirect("recommend-food-recipe", repas.id)
    return render(request, template_name="recommendation/recommend-food.html", context={
        "form": form,
    })

def recommendFoodRecipe(request, id):
    recette = Recette()
    repas = Repas.objects.get(pk=id)
    recette.repas = repas
    form = RecommendFoodRecipeForm(instance=recette)
    if request.method == "POST":
        form = RecommendFoodRecipeForm(request.POST, request.FILES, instance=recette)
        if form.is_valid():
            recette = form.save(commit=False)
            recette.repas = repas
            recette.save()
            return redirect("recommend-food-recipe-aliment", repas.id)
    form.fields["repas"].widget.attrs["disabled"] = True
    return render(request, template_name="recommendation/recommend-food-recipe.html", context={
        "form": form,
        "repas": repas
    })

def recommendFoodRecipeAliment(request, id):
    alimentRecette = AlimentRecette()
    recette = Recette.objects.get(repas__pk=id)
    alimentRecette.recette = recette
    form = RecommendFoodRecipeAlimentForm(instance=alimentRecette)
    saved = False
    if request.method == "POST":
        form = RecommendFoodRecipeAlimentForm(request.POST, request.FILES, instance=alimentRecette)
        if form.is_valid():
            alimentRecette = form.save(commit=False)
            alimentRecette.recette = recette
            saved = True
    form.fields["recette"].widget.attrs["readonly"] = True
    return render(request, template_name="recommendation/recommend-food-recipe-aliment.html", context={
        "form": form,
        "saved": saved,
        "recette":recette
    })

def recommendAliment(request):
    form = RecommendAlimentForm(instance=Aliment())
    saved = False
    if request.method == "POST":
        form = RecommendAlimentForm(request.POST, request.FILES, instance=Aliment())
        if form.is_valid():
            aliment = form.save(commit=False)
            aliment.contributeur = getUser(request.session)
            aliment.save()
            form = RecommendAlimentForm(instance=Aliment())
            saved = True
    return render(request, template_name="recommendation/recommend-aliment.html", context={
        "form": form,
        "saved":saved
    })
def recommendRestaurant(request):
    form = RecommendRestaurantForm(instance=Restaurant())
    saved = False
    if request.method == "POST":
        form = RecommendRestaurantForm(request.POST, request.FILES, instance=Restaurant())
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.contributeur = getUser(request.session)
            restaurant.save()
            form = RecommendRestaurantForm(instance=Restaurant())
            saved = True
    return render(request, template_name="recommendation/recommend-restaurant.html", context={
        "form": form,
        "saved":saved
    })
def rules(request):
	return render(request, template_name="recommendation/rules.html");