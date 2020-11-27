from django.forms import ModelForm
from django import forms

from .models import Listing, Bid, Comment


class ListingForm(ModelForm):
    class Meta:

        model = Listing
        exclude = ["created", "active", "creator"]

        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control", 'placeholder': "e.g. Wristwatch"}),
           'description': forms.Textarea(attrs={'class': "form-control", "rows": "6"}),
           'bid': forms.NumberInput(attrs={'class': 'form-control'}),
           "category": forms.Select(attrs={"class": "form-control"}),
        }



class BidForm(ModelForm):
    class Meta:

        model = Bid
        exclude = ["user", "listing"]

        widgets = {"bid": forms.NumberInput(attrs={"class": "form-control"})}


class CommentForm(ModelForm):
    class Meta:

        model = Comment
        exclude = ["user", "listing"]

        widgets = {"comment": forms.Textarea(attrs={"class": "form-control", "rows": "6"})}

