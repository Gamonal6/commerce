from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="new"),
    path("<str:listing>/listings", views.current_listing, name="clisting"),
    path("<int:listing_id>/addWatchlist", views.addWatchlist, name="addWatchlist"),
    path("<int:listing_id>/remWatchlist", views.remWatchlist, name="remWatchlist"),
    
]
