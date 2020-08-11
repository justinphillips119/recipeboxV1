from django.shortcuts import render, HttpResponseRedirect, reverse
from recipebook.models import Recipe 
from recipebook.models import Author
from recipebook.forms import AddRecipeForm, AddAuthorForm

def index(request):
    my_title = Recipe.objects.all()
    return render(request, "index.html", {"title": my_title, "welcome_name": 'World'})


def recipe_detail(request, recipe_id):
    my_title = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_title})

def author_viber(request, author_id):
    my_title = Author.objects.filter(id=author_id).first()
    return render(request, "author.html", {"author": my_title})

def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio'),
            )
            return HttpResponseRedirect(reverse("homepage"))



    form = AddAuthorForm()
    return render(request, "add_author.html", {'form': form})

def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                time_required=data.get('time_required'),
                description=data.get('description'),
                instruction=data.get('instruction'),
                author=data.get('author'),
            )
            return HttpResponseRedirect(reverse("homepage"))



    form = AddRecipeForm()
    return render(request, "add_recipe.html", {'form': form})