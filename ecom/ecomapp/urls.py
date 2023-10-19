from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
     path('search/', views.search_suggestions, name='search_suggestions'),
    path('register/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('create_order/', views.create_order, name='create_order'),
    ]