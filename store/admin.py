from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(UserCheckout)
