from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .forms import ListingForm


def index(request):

    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):

    if request.method == "GET":
        # A new Django form
        form = ListingForm()

        return render(request, "auctions/create.html", {'form': form})

    else:
        # A new Listing instance but with only value for creator field
        listing = Listing(creator=request.user)

        # A new form with submitted data from user and value for creator field
        form = ListingForm(request.POST, request.FILES, instance=listing)

        # If data is valid:
        if form.is_valid():
            # Insert data into database
            form.save()

            # Redirect to index view
            return HttpResponseRedirect(reverse("index"))

        # If data is not valid:
        else:

            return render(request, "auctions/create.html", {"form": form})


def listing(request, ID):

    if request.method == "GET":

        # Try and get the listing with id of ID
        try:
            listing = Listing.objects.get(id=ID)

        # If listing does not exist
        except Listing.DoesNotExist:
            # Render error page
            return render(request, "auctions/error.html", {"message": "The listing you requested does not exist."})

        # Get listing creator
        creator = User.objects.get(pk=listing.creator_id)

        # Render page for listing
        return render(request, "auctions/listing.html", {"listing": listing, "creator": creator})



def add_watchlist(request, listing):
    




