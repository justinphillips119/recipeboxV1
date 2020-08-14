from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from recipebook.models import Recipe 
from recipebook.models import Author
from recipebook.forms import AddRecipeForm, AddAuthorForm, AddLoginForm, AddSignupForm

def index(request):
    my_title = Recipe.objects.all()
    return render(request, "index.html", {"title": my_title, "welcome_name": 'World'})


def recipe_detail(request, recipe_id):
    my_title = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_title})

def author_viber(request, author_id):
    my_title = Author.objects.filter(id=author_id).first()
    return render(request, "author.html", {"author": my_title})

@login_required
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
                author=request.user,
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