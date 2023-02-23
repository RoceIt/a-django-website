import logging

from .cart import Cart

logger = logging.getLogger(__name__)

class CartMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['cart'] = Cart(request.session.get('cart', None))
        response = self.get_response(request)

        return response
