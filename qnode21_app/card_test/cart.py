from decimal import Decimal
from django.conf import settings
from courses_exams.models import Test


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        test_ids = self.cart.keys()
        # get the product objects and add them to the cart
        tests = Test.objects.filter(id__in=test_ids)

        cart = self.cart.copy()
        for test in tests:
            cart[str(test.id)]['test'] = test

        for item in cart.values():
            item['value'] = Decimal(item['value'])
            item['total_value'] = item['value'] * item['correct']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['correct'] for item in self.cart.values())

    def add(self, test, correct=1, update_correct=False):
        """
        Add a product to the cart or update its quantity.
        """
        test_id = str(test.id)
        if test_id not in self.cart:
            self.cart[test_id] = {'correct': 0,
                                      'value': str(test.value)}
        if update_correct:
            self.cart[test_id]['correct'] = correct
        else:
            self.cart[test_id]['correct'] += correct
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, test):
        """
        Remove a product from the cart.
        """
        test_id = str(test.id)
        if test_id in self.cart:
            del self.cart[test_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['value']) * item['correct'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
