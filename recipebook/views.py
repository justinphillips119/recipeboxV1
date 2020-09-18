from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from recipebook.models import Recipe 
from recipebook.models import Author
from recipebook.forms import AddRecipeForm, AddAuthorForm, AddLoginForm, AddSignupForm
from django.http import HttpResponseForbidden
from django import forms

def index(request):
    my_title = Recipe.objects.all()
    return render(request, "index.html", {"title": my_title, "welcome_name": 'World'})


def recipe_detail(request, recipe_id):
    my_title = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_title})

def author_viber(request, author_id):
    my_title = Author.objects.filter(id=author_id).first()
    my_recipes = Recipe.objects.filter(author=author_id)
    favorites = Recipe.objects.filter(id__in=my_title.favorites.all())
    return render(request, "author.html", {"author": my_title, "recipes": my_recipes, "favorites": favorites})

@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get('username'), password=data.get('password'))
                Author.objects.create(
                    name=data.get('name'),
                    bio=data.get('bio'),
                    user=new_user,   
                )
                return HttpResponseRedirect(reverse("homepage"))
    else:
        return HttpResponseForbidden("You don't have permission to add an author...")
    form = AddAuthorForm()
    return render(request, "generic_form.html", {'form': form})

@login_required
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
                author=request.user.author,
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AddLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))
                
    form = AddLoginForm()
    return render(request, "generic_form.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = AddSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    form = AddSignupForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


@login_required
def edit_recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data["title"]
            #recipe.author = data["author"]
            recipe.description = data["description"]
            recipe.time_required = data["time_required"]
            recipe.instruction = data["instruction"]
            recipe.save()
        return HttpResponseRedirect(reverse(recipe_detail, args=[recipe.id]))
    data = {
        "title": recipe.title,
        #"author": recipe.author,
        "description": recipe.description,
        "time_required": recipe.time_required,
        "instruction": recipe.instruction
    }

    form = AddRecipeForm(initial=data)
    if not request.user.is_staff:
        form.fields["author"] = forms.ModelChoiceField(
            queryset=Author.objects.filter(name=request.user.author)
        )
    return render(request, "generic_form.html", {"form": form})



def favorites_view(request, recipe_id):
    current_user = Author.objects.get(user__username=request.user.username)
    current_user.favorites.add(Recipe.objects.get(id=recipe_id))
    current_user.save()
    return HttpResponseRedirect(reverse("homepage"))


"""
def add_favorite_view(request, recipe_id):
    user = Author.objects.get(user=request.user)
    new_fav = Recipe.objects.filter(id=recipe_id).first()
    user.favorites.add(new_fav)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def remove_favorite_view(request, recipe_id):
    user = Author.objects.get(user=request.user)
    fav_recipe = Recipe.objects.filter(id=recipe_id).first()
    user.favorites.remove(fav_recipe)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
"""