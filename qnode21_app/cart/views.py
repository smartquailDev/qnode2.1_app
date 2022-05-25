from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from courses_exams.models import Test
from .cart import Cart
from .forms import CartAddTestForm


@require_POST
def cart_add(request, test_id):
    cart = Cart(request)
    test = get_object_or_404(Test, id=test_id)
    form = CartAddTestForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(test=test,
                 correct=cd['correct'],
                 update_correct=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, test_id):
    cart = Cart(request)
    test = get_object_or_404(Test, id=test_id)
    cart.remove(test)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
            item['update_correct_form'] = CartAddTestForm(
                              initial={'correct': item['correct'],
                              'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
