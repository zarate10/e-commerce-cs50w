from django.db import models
from django.contrib.auth.models import User 

# model for dynamic categories 
class Categories(models.Model): 
    title = models.TextField()
    def __str__(self):
        return self.title

CATEGORIES_PRODUCTS = []

dynamic_categories = Categories.objects.values()

for category in dynamic_categories: 
    CATEGORIES_PRODUCTS.append((category['title'], category['title']))


# model for products and bids
class Products(models.Model): 
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    initial_offer = models.PositiveIntegerField(blank=False)
    img_url = models.URLField()
    available = models.BooleanField(default=True) 
    category = models.CharField(max_length=150, choices=CATEGORIES_PRODUCTS, default=CATEGORIES_PRODUCTS[0])
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_offer = models.PositiveIntegerField(null=True, blank=True)
    last_bidder = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.owner.username + ' - ' + self.title

# model for comments
class Comments(models.Model): 
    user = models.CharField(max_length=150)
    comment = models.CharField(max_length=200)
    product = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user + ' - ' + self.comment

# model for watchlist
class WatchList(models.Model): 
    user = models.CharField(max_length=150)
    product = models.PositiveIntegerField()

