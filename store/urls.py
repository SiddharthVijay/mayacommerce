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
    path('index/', index, name='index'),
    path ('loagin/', login, name='login'),
    path ('category/<str:id>/', category, name='category'),
    path ('products/<str:id>/', products, name='products'),
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),


]
