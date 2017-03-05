from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import RecommendationForm
from . import algorithem

# Create your views here.
def home(request):
    '''
    Based on the Http Request, return the recommendations page. 
    we render either the recommendation met page or the recommendation not met page
    Input: Http request
    Output: Http Request with the html page and the context we want the html
    page to render
    '''
    
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
      
        if form.is_valid():
            data = form.cleaned_data
            template = 'results.html'
            criteris_met, context = algorithem.foof(data)
            #Criteria met show this page
            if criteris_met:
            	return render(request, template, context)
            #Criteria NOT met show this page
            else:
            	template = 'noresults.html'
            	return render(request, template, context)

    else:    
        form = RecommendationForm()
        template = 'home.html'
        context = {'form':form}
    return render(request, template, context)

