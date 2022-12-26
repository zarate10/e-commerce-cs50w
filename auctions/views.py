from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm, CreateNewProduct
from .models import Products, Comments, WatchList, Categories

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
    user_watchlist = list(WatchList.objects.filter(user=request.user.id, product=list(product.values())[0]['id']).values())

    contexto = {
        "name": name_view, 
        "watchlist": user_watchlist, 
        "product": product, 
        "active": product.values()[0]['available'],
    }

    if request.method == 'POST':
        oferta_inicial = int(product_obj['initial_offer']) 
        ultima_oferta = int(request.POST['last_offer']) 

        if product_obj['last_offer'] != None: # acá hay última oferta

            if int(product_obj['last_offer']) > ultima_oferta - 1: 

                contexto['message'] = "Bid must be higher than the last bid."
                return render(request, 'product_view.html', contexto) 
            
            product.update(last_offer=request.POST['last_offer'], last_bidder=request.POST['last_bidder'])
            return redirect(f'/product/{name}')

        else: # acá no hay última oferta
  
            if oferta_inicial > ultima_oferta - 1: 
                contexto['message'] = "The offer must be higher than the initial offer."
                return render(request, 'product_view.html', contexto) 
        
            product.update(last_offer=request.POST['last_offer'], last_bidder=request.POST['last_bidder'])
            return redirect(f'/product/{name}')

    if comments: 
        contexto['comments'] = comments

    if not contexto['active'] and request.user != 'AnonymousUser': 
        try: 
            contexto['ultimo_postor'] = list(User.objects.filter(id=request.user.id).values())[0]['username'] == product.values()[0]['last_bidder']
        except Exception as e:
            print(e)

    return render(request, 'product_view.html', contexto) 
    


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

def add_watchlist(request, name): 

    if request.method == 'POST': 
        user = request.POST['user']
        id_item = request.POST['item']

        data_in_database = WatchList.objects.filter(user=user, product=id_item)

        if not data_in_database: 
            WatchList.objects.create(
                user=user, 
                product=id_item
            )
        else: 
            data_in_database.delete()

    return redirect(f'/product/{name}')

def view_watchlist(request): 
    user_watchlist = [element[2] for element in list(WatchList.objects.filter(user=request.user.id).values_list())]
    products = [Products.objects.get(id=element) for element in user_watchlist]

    return render(request, 'watchlist.html', { 
        "name": "Watchlist",
        "products": products
    })

def inactive_products(request): 
    products = Products.objects.filter(available=False)

    contexto = {
        "products": products, 
    }

    try: 
        contexto['ultimo_postor'] = list(User.objects.filter(id=request.user.id).values())[0]['username'] == products.values()[0]['last_bidder']
    except Exception as e:
        print(e)

    return render(request, 'inactive.html', contexto)

def desactivar_producto(request, name): 
    
    if request.method == 'POST':
        product = Products.objects.filter(id=request.POST['item_id'])
        product.update(available=False)

    return redirect('/')

def view_categories(request): 

    categories = [element[1] for element in list(Categories.objects.all().values_list())]

    contexto = {
        "name": 'Categories', 
        "tipos": categories
    }

    return render(request, 'categories.html', contexto)

def filter_category(request, name): 

    products = Products.objects.filter(category=name, available=True)
    return render(request, "index.html", {
        "name": name, 
        "products": products, 
        "products_on_category": list(products)
    })

def view_create_offer(request): 

    if request.method == 'POST': 

        Products.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            initial_offer = request.POST['initial_offer'],
            img_url = request.POST['img_url'],
            category = request.POST['category'],
            owner_id = request.user.id
        )

    return render(request, "create_offer.html", {
        "name": "Create", 
        "form": CreateNewProduct
    })