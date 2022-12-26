from django.urls import path 
from . import views

urlpatterns = [ 
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('product/<str:name>', views.product_view, name="product_view"),
    path('product/<str:name>/', views.comments_view, name="comments_view"),
    path('product/<str:name>/watchlist', views.add_watchlist, name="add_watchlist"),
    path('product/<str:name>/inactive', views.desactivar_producto, name="desactivar_producto"),
    path('watchlist', views.view_watchlist, name="view_watchlist"),
    path('inactive', views.inactive_products, name="inactive_products"), 
    path('categories', views.view_categories, name="view_categories")
]