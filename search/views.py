# Code substantially modified, made reading the documentation at 
# https://docs.djangoproject.com/en/1.10/ref/class-based-views/base/
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import RecommendationForm
from . import algorithm

def home(request):
    
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
      
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            template = 'results.html'
            criteris_met, context = algorithm.recommend(data)
            #Criteria met show result.html page
            if criteris_met:
            	return render(request, template, context)
            #Criteria NOT met show noresult.html page
            else:
            	template = 'noresults.html'
            	return render(request, template, context)
    else:    
        form = RecommendationForm()
        template = 'home.html'
        context = {'form':form}
    return render(request, template, context)



