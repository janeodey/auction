from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.core.validators import FileExtensionValidator, MinValueValidator




class User(AbstractUser):

    def __str__(self):
        return f"{self.username.capitalize()}"




class Listing(models.Model):

    categories = [
        ("Groceries", "Groceries"),
        ("Health & Beauty", "Health & Beauty"),
        ("Home & Office", "Home & Office"),
        ("Phones & Tablets", "Phones & Tablets"),
        ("Computing","Computing"),
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Baby Products", "Baby Products"),
        ("Gaming", "Gaming"),
        ("Sporting Goods", "Sporting Goods"),
        ("Automobile", "Automobile"),
        ("Other", "Other")
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    bid = models.FloatField(default=0.00)
    category = models.CharField(max_length=50, null=False, choices=categories)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    created = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)
    image = models.ImageField(blank=False, validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])], upload_to="pictures/")

    def __str__(self):
        return f"{self.title} : {self.bid}"




class Bid(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, related_name="item")
    bid = models.FloatField(validators=[MinValueValidator(0.00)], null=True, blank=True)

    def __str__(self):
        return f"{self.listing.title} - {self.bid}"



class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=250)

    def __str__(self):

        return f"{self.user.username.capitalize()}"



class Watchlist(models.Model):

    item = models.ForeignKey("Listing", on_delete=models.CASCADE, blank=True, related_name="+")
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")





