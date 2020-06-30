import requests
from django.shortcuts import render
from bs4 import BeautifulSoup

# Create your views here.
def home (request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('Buscar')
    
    #en esta variable guardo todo lo que mandan del frontend
    cosas_del_frontend = {
        'buscar' : search,
    }

    return render(request,'myapp/new_search.html', cosas_del_frontend)