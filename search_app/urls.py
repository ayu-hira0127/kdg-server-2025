from django.urls import path
from . import views
from django.urls import path, include 

app_name = 'search_app'

urlpatterns = [
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/', views.product_list, name='product_list'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorite/<int:pk>/', views.favorite_product, name='favorite_product'),
    path('exhibited/', views.exhibited_list, name='exhibited_list'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('purchase/', views.purchase, name='purchase'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('', views.search, name='search_view'),
]