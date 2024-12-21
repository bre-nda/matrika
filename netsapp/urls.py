from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('mattresses/', views.mattress_page, name='mattress_page'),
    path('quilted-mattresses/', views.quilted_mattress_page, name='quilted_mattress_page'),
    path('plain-mattresses/', views.plain_mattress_page, name='plain_mattress_page'),
    path('mattresses/<str:type>/<int:thickness>/', views.mattress_detail, name='mattress_detail'),

    path('bedding/', views.bedding_page, name='bedding_page'),
]