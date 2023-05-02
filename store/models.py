from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    category_id = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=50,decimal_places=2)
    subcategory_id = models.ForeignKey("SubCategories", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    profile_pic = models.ImageField(upload_to='products/',blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='user/',blank=True)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    def __str__(self):
        return self.item.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    items = models.ManyToManyField("Product", through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    currency = models.CharField(max_length=50, default='Cad')
    subtotal = models.DecimalField(
        max_digits=50, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    # discounts
    # shipping

    def __str__(self):
        return str(self.id)





class UserCheckout(models.Model):
    Completed = 'Completed'
    Pending = 'Pending'
    Status = (
        (Completed, 'Completed'),
        (Pending, 'Pending')
    )
    stars = models.CharField(max_length=100, choices=Status, default=Pending)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, unique=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=250)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=250)

    def __str__(self):
        return self.first_name+' '+self.last_name
