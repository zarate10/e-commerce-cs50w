from django.urls import path 
from . import views

urlpatterns = [ 
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('product/<str:name>', views.product_view, name="product_view"),
]