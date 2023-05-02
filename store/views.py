from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from django.core import serializers
import json
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, permission_required


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views import View




from .models import *

# Create your views here.

context = {'categories' : Categories.objects.all()}
context['subcategories'] = SubCategories.objects.all()




def AddCart(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        request.session.set_expiry(0)
        cart_id = request.session.get('cart_id')
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

        if request.user.is_authenticated:
            print(request.user)
            cart.user = request.user
            cart.save()
        else:
            pass

        item_id = request.POST.get('item')
        delete_item = request.POST.get('delete')
        if item_id:
            item_instance = get_object_or_404(Product, id=item_id)
            qnt = request.POST.get('qnt')
            cart_item = CartItem.objects.get_or_create(cart=cart, item=item_instance)[0]
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qnt
                cart_item.save()



        messages.success(request, 'Cart Item Saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def index(request):
    request.session.set_expiry(0)
    context['cart_count'] = 0

    #prod_no = products.count()

    cart_id = request.session.get('cart_id')
    """
    if cart_id == None:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
    request.user.is_authenticated():

    cart = Cart.objects.get(pk=cart_id)
    cart_count = cart.cartitem_set.count()
    cart_items = cart.cartitem_set.all()
"""

    return render(request,'index.html',context)


"""
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)
"""

class MyLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


def checkout(request, id):
    context['product'] = Product.objects.get(id=id)
    context['subcategory'] = SubCategories.objects.get(id=context['product'].subcategory_id_id)
    context['category'] = Categories.objects.get(id=context['subcategory'].category_id_id)

    return render(request,'checkout.html',context)



@login_required(login_url='../../login/')
def login(request):
    title = 'Login and Register '
    cart_id = request.session.get('cart_id')
    context = {
        'title': title
    }

    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 == pass2:

            user = User.objects.create(
                username=uname,
                email=email,
                password=pass1
            )
            """
            if cart_id == None:
                cart = Cart()
                cart.user = user
                cart.save()
                cart_id = cart.id
                request.session['cart_id'] = cart_id
            cart = Cart.objects.get(pk=cart_id)
            cart.user = user
            cart.save()
            """

            messages.success(request, 'Featured Product Saved')
            return redirect('index')
    else:
        return render(request, 'login.html', context)



def category(request, id):
    context['subcategory'] = SubCategories.objects.get(id=id)
    context['products'] = Product.objects.filter(subcategory_id=id)
    return render(request,'category.html', context)


def products(request, id):
    context['product'] = Product.objects.get(id=id)
    context['subcategory'] = SubCategories.objects.get(id=context['product'].subcategory_id_id)
    context['category'] = Categories.objects.get(id=context['subcategory'].category_id_id)

    return render(request,'products.html',context)
