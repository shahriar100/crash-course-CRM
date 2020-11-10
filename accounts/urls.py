from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='dashboard'),
    path('user', views.userPage, name='user-page'),
    path('products/', views.products, name='products'),
    path('customer/<int:pk_test>/', views.customer, name='customer'),

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),
    path('create_order_by_id/<str:pk>', views.createOrderById, name='create_order_by_id'),

    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<str:pk>', views.updateCustomer, name='update_customer'),

    path('create_product/', views.createProduct, name='create_product'),
]
