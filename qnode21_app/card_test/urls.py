from django.urls import path
from . import views

app_name = 'card_test'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:test_id>/',
         views.cart_add,
         name='cart_add'),
    path('remove/<int:test_id>/',
         views.cart_remove,
         name='cart_remove'),
]
