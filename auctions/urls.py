from django.urls import path
from django.conf.urls.static import static

from . import views

#app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:ID>", views.listing, name="listing"),
    path("add/watchlist<int:listing>", views.add_watchlist, name="add"),
    path("delete/watchlist<int:listing>", views.delete_watchlist, name="delete"),
    path("close/<int:ID>", views.close_listing, name="close"),
    path("watchlist/<str:user>", views.watchlist, name="watchlist"),
    path("category/<str:group>", views.category, name="category")
]



