from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.validators import MinValueValidator
from django import forms
from django.contrib.auth.models import AnonymousUser

from .models import User, Listing, Watchlist, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm




def index(request):

    listings = Listing.objects.all().filter(active=True)

    dic = {}

    i = 1
    for listing in listings:
        dic[f"{i}"] = listing
        i += 1

    return render(request, "auctions/index.html", {"listings": listings, "badge": badge_count(request), "dic": dic})





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

        return render(request, "auctions/create.html", {'form': form, "badge": badge_count(request)})

    else:
        # A new Listing instance but with only value for creator field
        listing = Listing(creator=request.user)

        # A new form with submitted data from user and value for creator field
        form = ListingForm(request.POST, request.FILES, instance=listing)

        # If data is valid:
        if form.is_valid():
            # Save item, but don't insert into database yet.
            # The essence of this is to get the listing instance that will be returned when commit=False.
            listing_instance = form.save(commit=False)

            # Insert into database
            listing_instance.save()

            # Insert new bid for the new listing. This bid is the bid the creator set, by default it's 0.00
            Bid.objects.create(user=request.user, listing=listing_instance, bid=request.POST["bid"])

            # Redirect to index view
            return HttpResponseRedirect(reverse("index"))

        # If data is not valid:
        else:
            return render(request, "auctions/create.html", {"form": form, "badge": badge_count(request)})





# Function for watchlist badge
def badge_count(request):
    try:
        badge = len(Watchlist.objects.all().filter(user=request.user))
        return badge
    except:
        return None





def listing(request, ID):

    if request.method == "GET":

        # Try and get the listing with id of ID
        try:
            listing = Listing.objects.get(id=ID)

        # If listing does not exist
        except Listing.DoesNotExist:
            # Render error page
            return render(request, "auctions/error.html", {"message": "The listing you requested does not exist.",
                "badge": badge_count(request)})

        # This is to know if this listing is already in user's watchlist
        # and so change "add to watchlist" button to remove
        try:
            if Watchlist.objects.filter(item=listing, user=request.user).exists():
                remove = True
            else:
                remove = False
        except:
            remove = 4895

        comments = Comment.objects.filter(listing=listing).order_by("-id")

        try:
            current_bid = Bid.objects.filter(listing=listing).order_by("-id").first().bid
        except:
            current_bid = 0.00

        # New BidForm and CommentForm for listing
        form = None
        co_form = None
        if request.user.is_authenticated:
            form = BidForm(initial={"bid": current_bid})
            co_form = CommentForm()

        # If listing is closed, get highest bidder
        winner = None
        if listing.active == False:
            winner = Bid.objects.filter(bid__gt=0).order_by("-bid").first()

        # Render page for listing
        return render(request, "auctions/listing.html", {"listing": listing, "badge": badge_count(request),
            "remove": remove, "form": form, "winner": winner, "co_form": co_form, "comments": comments})

    else:
        # Get listing item and current bid for it
        listing = Listing.objects.get(id=ID)
        try:
            current_bid = Bid.objects.filter(listing=listing).order_by("-id").first().bid
        except:
            current_bid = 0

        # If bid form was submitted
        if "bid" in request.POST:

            # If posted bid is less than or equal to current bid
            if float(request.POST["bid"]) <= current_bid or request.POST["bid"] is None:
                return render(request, "auctions/error.html", {"message": "Your bid should be more than the curent bid.", "badge": badge_count(request)})

            # A Bid model object with values for user and listing
            instance = Bid(user=request.user, listing=listing)

            # A bid form populated with posted bid and values from the Bid model object
            form = BidForm(request.POST, instance=instance)

            # If bid form is valid
            if form.is_valid():

                # Save into database
                form.save()

                # Update bid of listing in Listing table
                listing.bid = Bid.objects.filter(listing=listing, user=request.user).order_by("-id").first().bid

                # Save into database
                listing.save()

        # If comment form was submitted
        if "comment" in request.POST:

            # A Comment model with values for user and listing
            co_instance = Comment(user=request.user, listing=Listing.objects.get(id=ID))

            # A comment form populated with posted comment and values from the Comment model object
            co_form = CommentForm(request.POST, instance=co_instance)

            # If form is valid
            if co_form.is_valid():

                # Save into database
                co_form.save()

        return HttpResponseRedirect(reverse("listing", args=[ID]))





@login_required
def add_watchlist(request, listing):

    # Do some error checking, like if listing doesn't exist in database

    # Get listing object
    listing = Listing.objects.get(id=listing)

    # Insert listing object into watchlist table
    new = Watchlist(item=listing, user=request.user)
    new.save()

    return HttpResponseRedirect(reverse("listing", args=[listing.id]))





@login_required
def delete_watchlist(request, listing):

    # Do some error checking, like if listing doesn't exist in database

    # Get listing object and delete from watchlist table
    Watchlist.objects.filter(item_id=Listing.objects.get(id=listing)).delete()

    return HttpResponseRedirect(reverse("listing", args=[listing]))





@login_required
def close_listing(request, ID):

    # Get listing
    listing = Listing.objects.get(id=ID)

    # If listing wasn't created by request
    if listing.creator != request.user:
        return render(request, "auctions/error.html", {"message": "Forbidden. You can't perform this action."})

    # Close listing
    listing.active = False

    # Update in database
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=[ID]))





def watchlist(request, user):

    # Do some error checking, like if user doesn't exist

    # Get user
    user = User.objects.get(username=user)

    # Get watchlist items of user
    items = Watchlist.objects.filter(user=user).order_by("-id")

    return render(request, "auctions/watchlist.html", {"items": items, "badge": badge_count(request)})




def category(request, group):

    # Get listings in category
    listings = Listing.objects.filter(category=group)

    return render(request, "auctions/category.html", {"listings": listings, "badge": badge_count(request), "group": group})




