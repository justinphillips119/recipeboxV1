from django.shortcuts import render
from recipebook.models import Recipe, Author

def index(request):
    my_title = Recipe.objects.all()
    return render(request, "index.html", {"title": my_title, "welcome_name": 'World'})


def recipe_detail(request, recipe_id):
    my_title = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_title})

def author_viber(request, author_id):
    my_title = Author.objects.filter(id=author_id).first()
    return render(request, "author.html", {"author": my_title})
