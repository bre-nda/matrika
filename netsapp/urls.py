from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

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
    # path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    re_path(r'^cart/delete/(?P<cart_item_id>[\w-]+)/$', views.delete_cart_item, name='delete_cart_item'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('search/', views.search_products, name='search_products'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]