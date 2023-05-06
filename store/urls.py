from django.urls import path,include
from .views import *
from django.contrib.auth.views import LoginView


from .views import MyLoginView#, RegisterView, MyProfile #, profile



from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path('', index, name='index'),
    path('add/', AddCart, name='AddCart'),
    path('cart_edit/', EditCart, name='EditCart'),
    path('cartcount/', CartCount, name='CartCount'),
    path('index/', index, name='index'),
    path('checkout/', checkout, name='checkout'),
    path('viewcart/', viewcart, name='viewcart'),
    path('payment/', Payment, name='payment'),
    path('payment_redirect/', payment_redirect, name='payment_redirect'),
    path('checkoutcommit/', CheckoutCommit, name='payment'),

    path ('loagin/', login, name='login'),
    path ('category/<str:id>/', category, name='category'),
    path ('products/<str:id>/', products, name='products'),
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),


]
