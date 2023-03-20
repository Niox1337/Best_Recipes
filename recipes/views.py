from django.shortcuts import render


# Create your views here.

def index(request):
    trending = {'trending': 'Trending'}
    return render(request, 'recipes/index.html', context=trending)
