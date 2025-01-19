from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('mattresses/', views.mattress_page, name='mattress_page'),
    path('quilted-mattresses/', views.quilted_mattress_page, name='quilted_mattress_page'),
    path('plain-mattresses/', views.plain_mattress_page, name='plain_mattress_page'),
    path('mattress/<str:type>/<int:thickness>/', views.mattress_detail, name='mattress_detail'),
    path('bedding/', views.bedding_page, name='bedding_page'),
    path('pillow/<int:pk>/', views.pillow_detail, name='pillow_detail'),
    path('duvet/<int:pk>/', views.duvet_detail, name='duvet_detail'),
    path('bedsheet/<int:pk>/', views.bedsheet_detail, name='bedsheet_detail'),
    path('cart/', views.cart_page, name='cart_page'),
    path('add-to-cart/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]