from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import io
import base64

import matplotlib
matplotlib.use('Agg')            # 1) Fijar backend ANTES de pyplot
import matplotlib.pyplot as plt


# Create your views here.
def home(request):
    #return HttpResponse('<h1> Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render (request, 'home.html',{'name': 'Juan Manuel Gallo López'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'movies': movies,
        'name': 'Juan Manuel Gallo López'
    })


def about(request):
    #return HttpResponse('<h1> Welcome to About Page </h1>')
    return render(request, 'about.html')

def signup(request):
    email=request.GET.get('email')
    return render(request, 'signup.html',{'email':email})

def statistics_view(request):
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Contar películas por año
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year is not None else 'N/A'
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    # Ordenar por año (dejando 'N/A' al final)
    items = list(movie_counts_by_year.items())
    items_sorted = sorted(items, key=lambda kv: (9999 if kv[0] == 'N/A' else kv[0]))

    labels = [str(k) for k, _ in items_sorted]
    counts = [v for _, v in items_sorted]
    positions = range(len(labels))

    # Crear la gráfica
    plt.figure()
    plt.bar(positions, counts, width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(positions, labels, rotation=90)
    plt.tight_layout()  # evita cortes en las etiquetas

    # Convertir a PNG en memoria y a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic = base64.b64encode(image_png).decode('utf-8')


    genre_counts = {}
    for m in all_movies:
        if m.genre:
            first_genre = m.genre.split(',')[0].strip()   # solo el primero
        else:
            first_genre = 'N/A'
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    # Ordenar alfabéticamente por género para un eje estable
    genre_items = sorted(genre_counts.items(), key=lambda kv: kv[0])
    genre_labels = [k for k, _ in genre_items]
    genre_values = [v for _, v in genre_items]
    genre_pos = range(len(genre_labels))

    # Crear la gráfica por género
    plt.figure()
    plt.bar(genre_pos, genre_values, width=0.5, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(genre_pos, genre_labels, rotation=90)
    plt.tight_layout()

    # Convertir a PNG en memoria y a base64
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    image_png2 = buffer2.getvalue()
    buffer2.close()
    plt.close()

    graphic_genre = base64.b64encode(image_png2).decode('utf-8')

    # Renderizar la plantilla con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic_genre': graphic_genre
    })

