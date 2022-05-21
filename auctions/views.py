import re
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Comments, Bids

def index(request):
    active_listings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


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
def newListing(request):
    if request.method == "GET":
        return render(request, "auctions/new_listing.html")
    else:
        current_user = request.user  #Gather the current user information to link to the listings database
        new_listing = request.POST
        new_bid = Bids(price = new_listing["bid"], bidder_id = current_user, title = new_listing["title"])
        new_bid.save()
        new_data = Listings(title=new_listing["title"], bids_id=new_bid, description=new_listing["description"], img_url=new_listing["img-url"], category=new_listing["category"], owner_id=current_user)
        new_data.save()
        return HttpResponseRedirect(reverse("index"))

def current_listing(request, listing):
    if request.method == "GET":
        cur = Listings.objects.filter(title=listing)
        cur_comments = Comments.objects.select_related('listing').filter(listing_id=cur[0].id)
        cur_user = str(cur[0].owner_id)
        watchlist = cur[0].watchlist.all()
        if request.user in watchlist:
            in_watchlist = True
        else:
            in_watchlist = False

        print(in_watchlist)
        return render(request, "auctions/listing.html", {
            "cur":cur[0],
            "cur_comments":cur_comments,
            "cur_user": cur_user,
            "in_watchlist": in_watchlist
        })

    else:
        cur = Listings.objects.filter(title=listing)

        new_comment = request.POST["comment"]
        store_comment = Comments(comment=new_comment, commenter=request.user, listing=cur[0])
        store_comment.save()
        return HttpResponse("It worked")
        

def addBid(request, listing_id):
    update_bids = Listings.objects.get(pk=listing_id)
    updateb = Bids.objects.filter(pk = update_bids.title).update(price = request.POST["bid"], bidder_id = request.user)
    
    return HttpResponse("It worked")

def addWatchlist(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)
    user.watchlist.add(listing)
    return HttpResponse("It worked")

def remWatchlist(request, listing_id):
    instance = User.objects.get(pk=request.user.id)
    listing = Listings.objects.get(pk=listing_id)
    instance.watchlist.remove(listing)
    return HttpResponse("It worked")

def closeListing(request, listing_id):
    listing = Listings.objects.filter(pk=listing_id)
    listing.update(is_open=False)
    return HttpResponse("It worked")

def ceategoryList(request):
    categories = ["Categorie1", "Categorie2", "Categorie3", "Categorie4"]
    return render(request, "auctions/categoryList.html", {
        "categories": categories
    })

def categorySearch(request, category):
    category_list = Listings.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "category_list": category_list
    })


def watchlist(request): 
    current_user = request.user
    users_watchlist = current_user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist":users_watchlist
    })