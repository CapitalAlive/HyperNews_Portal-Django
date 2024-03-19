from django import forms


class NewArticle(forms.Form):
    title = forms.CharField()
    text = forms.CharField()

