from django import forms 
from recipebook.models import Author, Recipe

class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=80)
    bio = forms.CharField(widget=forms.Textarea)
    


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=80)
    time_required = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    instruction = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())