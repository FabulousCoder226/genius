import uuid
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator 
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from main.models import *
from .forms import *

# Create your views here.

def home(request):
    meal = Category.objects.all()
    gift = Food.objects.filter(special_gifts=True)

    context = {
        'meal':meal,
        'gift':gift
    }
    return render(request, 'index.html', context)

def category(request, id, slug):
    brand = Category.objects.get(pk=id)
    categ = Food.objects.filter(type_id=id)

    context = {
        'brand':brand,
        'categ':categ
    }
    return render(request, 'category.html', context)

def products(request):
    product = Food.objects.all()
    p = Paginator(product, 6)
    page = request.GET.get('page')
    pagin = p.get_page(page)
    
    context = {
        'pagin':pagin
    }
    return render(request, 'products.html', context)

def contact(request):
    contact = ContactForm()
    if request.method == 'POST':
        contact = ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
            messages.success(request, 'your message has been sent successfully')
            return redirect('home')

    context = {
        'contact':contact
    }
    return render(request, 'contact.html', context)

# authenticate
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'you are now signed out')
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'you are now signed in successfully')
            return redirect('home')
        else:
            messages.error(request, 'username/password is incorrect please try again')
            return redirect('signin')

    return render(request, 'signin.html')

def signup(request):
    form = CustomerForm()
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']
        pix = request.POST['pix']
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            newuser = Customer(user=user)
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.email = user.email
            newuser.address = address
            newuser.phone = phone 
            newuser.pix = pix
            newuser.save() 
            messages.success(request, f'dear {user.username} your account is created successfully')
            return redirect('signin')
        else:
            messages.error(request, form.errors)

    return render (request, 'signup.html')

# authenticate done

@login_required(login_url='signin')
def profile(request):
    userprof = Customer.objects.get(user__username = request.user.username)

    context = {
        'userprof':userprof
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = ProfileForm(instance=request.user.customer)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            user = form.save()
            new = user.first_name.title()
            messages.success(request, f'dear {new} your profile update is successful')
            return redirect('profile')
        else:
            new = user.first_name.title()
            messages.error(request, f'dear {new} your profile update generated the following errors: {form.errors}')
            return redirect('profile_update')

    context = {
        'userprof':userprof
    }

    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        new = request.user.username.title()
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'dear {new} your password change is successful')
            return redirect('profile')
        else:
            messages.error(request, f'dear {new} the following error occured, {form.errors}')
            return redirect('password_update')

    context = {
        'userprof':userprof,
        'form':form
    }

    return render(request, 'password_update.html', context)

@login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        food = request.POST['foodid']
        main = Food.objects.get(pk=food)
        cart = Cart.objects.filter(user__username = request.user.username, paid=False)
        if cart:
            basket = Cart.objects.filter(user__username = request.user.username, paid=False, food = main.id, qty = quantity).first()
            if basket:
                basket.qty += quantity 
                basket.amount = main.price * basket.qty 
                basket.save()
                messages.success(request, 'one food item added to cart')
                return redirect('products')
            else:
                newitem = Cart()
                newitem.user = request.user
                newitem.food = main
                newitem.qty = quantity
                newitem.price = main.price
                newitem.amount = main.price * quantity
                newitem.paid = False
                newitem.save()
                messages.success(request, 'one food item added to cart')
                return redirect('products')
        else:
            newcart = Cart()
            newcart.user = request.user
            newcart.food = main
            newcart.qty = quantity
            newcart.price = main.price
            newcart.amount = main.price * quantity
            newcart.paid = False
            newcart.save()
            messages.success(request, 'one food item added to cart')
            return redirect('products')


@login_required(login_url='signin')
def cart(request):
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.qty
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.price * item.qty
        vat = 0.075 * subtotal
        total = subtotal + vat

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total
    }

    return render(request, 'cart.html', context)

def increase(request):
    if request.method == 'POST':
        qty_item = request.POST['quantid']      #item to be increased
        new_qty = request.POST['quant']         #number you want to increase to
        newqty = Cart.objects.get(pk=qty_item)
        newqty.qty = new_qty
        newqty.amount = newqty.price * newqty.qty
        newqty.save()
        messages.success(request, 'quantity updated')
        return redirect('cart')

def delete(request):
    if request.method == 'POST':
        del_item = request.POST['delid']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'one item deleted')
        return redirect('cart')

def checkout(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.qty
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.price * item.qty
        vat = 0.075 * subtotal
        total = subtotal + vat

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
        'userprof':userprof
    }

    return render(request, 'checkout.html', context)

def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_27a1166abccb107ea7d9f6ba54f3ebfee7520b00' #secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize' #paystack call url
        cburl = 'http://52.91.224.59/callback' #payment confirmation page
        ref = str(uuid.uuid4()) #reference number required by paystack as an additional order number
        profile = Customer.objects.get(user__username = request.user.username)
        order_no = profile.id #the main ordernumber
        total = float(request.POST['total']) * 100 #total amount to be charged from the customer card
        user = User.objects.get(username = request.user.username) #query the user model for customer details
        email = user.email #get customer email to send to paystack
        first_name = request.POST['first_name'] #collect from the template incase there is change
        last_name = request.POST['last_name'] #collect from the template incase there is change
        phone = request.POST['phone'] #collect from the template incase there is change
        add_info = request.POST['add_info'] #collect from the template incase there is change
        address = request.POST['address'] #collect from the template incase there is change

        #collect data to send to paystack via call
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':ref, 'amount':int(total), 'email':user.email, 'callback_url':cburl, 'order_number':order_no, 'currency':'NGN'}

        #Make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data) #pip install requests
        except Exception:
            messages.error(request, 'network busy, please try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Purchase()
            account.user = user
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.amount = total/100
            account.paid = True
            account.phone = phone 
            account.address = address
            account.additional_info = add_info
            account.pay_code = ref
            account.save()

            return redirect(rdurl)

    return redirect('checkout')

def callback(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid = False)

    for item in cart:
        item.paid = True                                               #item in cart page deletes
        item.save()

        food = Food.objects.get(pk=item.food.id)

    context = {
        'userprof':userprof,
        'cart':cart,
    }

    return render(request, 'callback.html', context)

def search(request):
    if request.method == 'POST':
        items = request.POST['search']
        searched = Q(Q(foodname__icontains=items)| Q(price__icontains=items))
        searched_item = Food.objects.filter(searched)

        context = {
            'items':items,
            'searched_item':searched_item
        }

        return render(request, 'search.html', context)

