from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:id>/<slug:slug>', views.category, name='category'),
    path('meals', views.products, name='products'),
    path('contact', views.contact, name='contact'),
    path('signout', views.signout, name='signout'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('password_update', views.password_update, name='password_update'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('increase', views.increase, name='increase'),
    path('delete', views.delete, name='delete'),
    path('checkout', views.checkout, name='checkout'),
    path('pay', views.pay, name='pay'),
    path('callback', views.callback, name='callback'),
    path('search', views.search, name='search'),
]