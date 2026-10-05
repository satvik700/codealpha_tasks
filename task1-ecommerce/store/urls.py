from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.product_list, name="product_list"),
    path("product/<int:pk>/", v.product_detail, name="product_detail"),
    path("cart/", v.cart, name="cart"),
    path("cart/add/<int:pk>/", v.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", v.cart_update, name="cart_update"),
    path("checkout/", v.checkout, name="checkout"),
    path("orders/", v.orders, name="orders"),
    path("register/", v.register, name="register"),
]
