import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGLIST_URL = 'https://buenosaires.craigslist.org/search/hhh?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home (request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('Buscar')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    
    response = requests.get(final_url)
    data = response.text
    
    #busca todos los links que tenga el titulo auto
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
        
    final_postings = []

    for post in post_listings:
        post_titles = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        #el data id de la pagina es un string asi que lo divido por comas y creo una lista
        #cada elemento de esa lista queda algo como 1:dfsadfk donde a mi me importa lo que esta despues de ':'
        #como quiero solo la primer imagen agarro el primer elemento de la lista y lo divido en una lista por ':'
        #la lista queda por un lado '1' y el otro 'dfsadfk', a mi me importa la segunda parte asi que la tengo con [1]    
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

    
        final_postings.append((post_titles,post_url,post_price, post_image_url))
    
    #en esta variable guardo todo lo que mandan del frontend
    cosas_del_frontend = {
        'buscar' : search,
        'final_postings' : final_postings,
        
    }

    return render(request,'myapp/new_search.html', cosas_del_frontend)