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
                cart_item.quantity += int(qnt)
                cart_item.line_item_total = cart_item.quantity*item_instance.amount
                cart_item.save()
                cart.total += cart_item.line_item_total
                cart.save()



        messages.success(request, 'Cart Item Saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def EditCart(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        request.session.set_expiry(0)
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        post = request.POST
        from_client = request.POST['send']
        from_client = json.loads(from_client)
        cart_amount=0
        for item in from_client:
            vari_id = int(item['id'])
            vari_obj = get_object_or_404(Product, pk=vari_id)

            cart_item = CartItem.objects.get_or_create(
                cart=cart,
                item=vari_obj
            )
            vari_del = item['del']
            qnt = int(item['qnt'])
            price = float(item['price'])
            line_total = qnt*price
            cart_item[0].line_item_total = line_total
            if vari_del == 'True' or qnt <= 0:
                cart_item[0].delete()
            else:
                cart_item[0].quantity = qnt
                cart_item[0].save()
            cart_amount+=line_total
        cart.total = cart_amount
        cart.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def CartCount(request):
    cart_id = request.session.get('cart_id')
    object = get_object_or_404(Cart, pk=cart_id)
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()
    data = serializers.serialize("json", cart_items)
    return HttpResponse(data, content_type='application/json')


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

        messages.add_message(self.request, messages.ERROR, "Invalid username or password",extra_tags='danger')
        return self.render_to_response(self.get_context_data(form=form))


def checkout(request):
#    context['product'] = Product.objects.get(id=id)
#    context['subcategory'] = SubCategories.objects.get(id=context['product'].subcategory_id_id)
#    context['category'] = Categories.objects.get(id=context['subcategory'].category_id_id)
    context['title'] = 'Checkout'
    context['cart_count'] = 0
    cart_id = request.session.get('cart_id')
    if cart_id:
        object = get_object_or_404(Cart, pk=cart_id)
        context['object'] = object

    return render(request,'checkout.html',context)



def viewcart(request):
    context['title'] = 'My Shopping Cart'
    context['cart_count'] = 0
    cart_id = request.session.get('cart_id')
    if cart_id:
        object = get_object_or_404(Cart, pk=cart_id)
        context['object'] = object
        context['cart_count'] = object.cartitem_set.count()
        context['cart_items'] = object.cartitem_set.all()


    return render(request, 'viewcart.html', context)




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


def CheckoutCommit(request):
    cart_id = request.session.get('cart_id')
    object = get_object_or_404(Cart, pk=cart_id)

    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        add1 = request.POST.get('address1')
        add2 = request.POST.get('address2')
        comp = request.POST.get('company')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zcode = request.POST.get('zip')
        user = None

        if request.user.is_authenticated:
            user = request.user
        uc = UserCheckout.objects.filter(cart=object)
        if uc:
            return redirect('/payment/')
        else:
            checkout = UserCheckout.objects.get_or_create(
                user=user,
                cart=object,
                first_name=fname,
                last_name=lname,
                email=email,
                phonenumber=phone,
                address1=add1,
                address2=add2,
                company=comp,
                country=country,
                state=state,
                city=city,
                zip_code=zcode
            )
            print(checkout)
            messages.success(request, 'Details Saved')
            return redirect('/payment/')
    return redirect('/payment/')


def Payment(request):
    title = 'Complete Payment'
    cart_id = request.session.get('cart_id')
    object = get_object_or_404(Cart, pk=cart_id)
    amount = object.total
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()
    checkout_obj = UserCheckout.objects.get(cart=object)
    #client_token = checkout_obj.get_client_token()
    context = {
        'title': title,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'checkout_obj': checkout_obj,
        'object': object,
        #'client_token': client_token

    }

    if request.method == 'POST':

        del request.session["cart_id"]
        checkout_obj.stars = 'Completed'
        checkout_obj.save()
        return redirect('/payment_redirect/')


    return render(request, 'payment.html', context)


def payment_redirect(request):
    context['message'] = "Payment Successful"
    return render(request,'payment_redirect.html', context)




def category(request, id):
    context['subcategory'] = SubCategories.objects.get(id=id)
    context['products'] = Product.objects.filter(subcategory_id=id)
    return render(request,'category.html', context)


def products(request, id):
    context['product'] = Product.objects.get(id=id)
    context['subcategory'] = SubCategories.objects.get(id=context['product'].subcategory_id_id)
    context['category'] = Categories.objects.get(id=context['subcategory'].category_id_id)

    return render(request,'products.html',context)
