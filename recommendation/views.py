from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, template_name="recommendation/index.html", context={})
def recommendFood(request):
    pass
def recommendAliment(request):
    pass
def recommendRestaurant(request):
    pass
def rules(request):
    pass