from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm
from .models import Products, Comments

# Create your views here.

def index(request):
    
    name_view = 'Home'
    products = Products.objects.filter(available=True)


    return render(request, "index.html", {
        "name": name_view, 
        "products": products
    })


def login_view(request):

    name_view = 'Login'

    if request.method != 'POST': 

        return render(request, 'login.html', {
            "form": AuthenticationForm, 
            "name": name_view
        })

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None: 
        login(request, user)
        return redirect('index')
    
    return render(request, 'login.html', {
        "form": AuthenticationForm, 
        "message": "The user or password is invalid.",
        "name": name_view
    })


def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):

    name_view = 'Register'

    if request.method != 'POST':

        return render(request, 'register.html', {
            "form": UserCreationForm, 
            "name": name_view
        })
    
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password1']
    confirmation = request.POST['password2']


    if password != confirmation:
        return render(request, "register.html", {
            "message": "Passwords must match.", 
            "name": name_view
        })

    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except:
        return render(request, "register.html", {
            "form": UserCreationForm,
            "message": "Username already taken.", 
            "name": name_view
        })

    login(request, user)
    return redirect("index")

def product_view(request, name):
    name_view = name
    product = Products.objects.filter(title=name)
    product_obj = product.values()[0]
    comments = list(Comments.objects.filter(product=product_obj['id']).values())

    print(comments)
    if request.method == 'POST':
        
        oferta_inicial = int(product_obj['initial_offer']) 
        ultima_oferta = int(request.POST['last_offer']) 

        if product_obj['last_offer'] != None: # acá hay última oferta

            if int(product_obj['last_offer']) > ultima_oferta - 1: 
                return render(request, 'product_view.html', {
                    "name": name_view, 
                    "product": product, 
                    "message": "Bid must be higher than the last bid."
                }) 
            
            product.update(last_offer=request.POST['last_offer'], last_bidder=request.POST['last_bidder'])
            return redirect(f'/product/{name}')

        else: # acá no hay última oferta
  
            if oferta_inicial > ultima_oferta - 1: 
                return render(request, 'product_view.html', {
                    "name": name_view, 
                    "product": product, 
                    "message": "The offer must be higher than the initial offer."
                }) 
            
            product.update(last_offer=request.POST['last_offer'], last_bidder=request.POST['last_bidder'])
            return redirect(f'/product/{name}')
        
        # print(request.POST['last_offer'])

    if comments: 

        return render(request, 'product_view.html', {
            "name": name_view, 
            "product": product, 
            "comments": comments, 
        }) 
    
    return render(request, 'product_view.html', {
        "name": name_view, 
        "product": product, 
    }) 
    


def comments_view(request, name): 

    product = Products.objects.filter(title=name)
    product_obj = product.values()[0]

    if request.method == 'POST': 

        comentario = request.POST['comment']

        if len(comentario) > 0: 

            Comments.objects.create(
                comment=comentario,
                product=product_obj['id'], 
                user=request.user
                )

            return redirect(f'/product/{name}')

    return redirect(f'/product/{name}')