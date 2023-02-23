
"""Adding the base

Had to define a string to represent no info because the cart is
transported by the session system as a json object which doesn't
know None and stored it as a json null value. This translation is
also why the __init__ has an update function.
"""
import logging
import json

import django.utils.timezone as tz
from collections import Counter, defaultdict
from django.utils.translation import ugettext_lazy as _


from . import forms
from . import models
#    OrderItem, DeliveryDateForDeliveryAddress, Order, OrderLine)
logger = logging.getLogger(__name__)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class RemoveError(Error):
    """Raised when a remove request is dubious.

    Attributes:
        item -- the item requested to be removed
        info -- the info about the item
        message -- explanation of why the remove is not allowed
    """

    def __init__(self, item, info, message):
        self.item = item
        self.info = info
        self.message = message


ALL = '_a_'
NO_INFO = '_no@info_'


class OrderInfo():

    NONE = '__NONE__'

    def __init__(self, initial="{}"):
        self.info = json.loads(initial)
        self._check_if_empty()

    def __str__(self):
        return json.dumps(self.info, sort_keys=True)

    def _check_if_empty(self):
        """Adds/removes an empty indicator to the info dictionary. """
        if not self.info:
            self.info = {self.NONE: 'True'}
        elif self.info.pop(self.NONE, None):
            self._check_if_empty()

    def __len__(self):
        if self.NONE in self.info:
            return 0
        return len(self.info)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __setitem__(self, key, value):
        assert isinstance(key, str)
        assert isinstance(value, str)
        assert not key == self.NONE
        self.info[key] = value
        self._check_if_empty()

    def __getitem__(self, key):
        return self.info.get(key)

    def __delitem__(self, key):
        del self.info[key]
        self._check_if_empty()

    def __contains__(self, key):
        return key in self.info


class Cart(defaultdict):
    """Simple shopping cart.

    Usage:
        Create a cart by instantiating the class. You can add extra information
        to the items you add.  You can check the number of items in the cart in
        different ways with the count function.
        Use remove items to remove a number of items from the cart by item or
        info.  Remove all items with clear.
        Calling len on the instance returns the total number of items in the
        Cart.

    methods:
        add_items -- add items to cart.
        remove_items -- remove items from cart.
        clear -- remove all items.
        __len__ -- gives the total number of items in the cart.
    """
    def __init__(self, initial_data=None):
        super().__init__(Counter)
        if initial_data is not None:
            self.update(initial_data)

    def add_items(self, item, nr_of_items, info=OrderInfo()):
        """Add nr_of_items of items to the cart.  If the item is already in
        the cart it is added to the items already added.  Info will be
        stored for the number of items it is referring to.

        """
        item, info = str(item), str(info)
        if info not in self[item]:
            self[item][info] = 0
        self[item][info] = self[item][info] + nr_of_items

    def remove_items(self, item, nr_of_items=0, info=OrderInfo()):
        """Remove item(s) from the cart.

        Usage:
        """
        item, info = str(item), str(info)
        if nr_of_items is ALL:
            if info is ALL:
                del self[item]
            else:
                del self[item][info]
        elif nr_of_items >= self[item][info]:
            del self[item][info]
            if len(self[item]) == 0:
                del self[item]
        else:
            self[item][info] -= nr_of_items

    def set_item(self, item, nr_of_items, info=OrderInfo()):
        """Set number of items.

        """
        item, info = str(item), str(info)
        count_before = self.count(item, info)
        if nr_of_items == 0:
            self.remove_items(item, ALL, info)
            return -count_before
        self[item][info] = nr_of_items
        return count_before - nr_of_items

    def count(self, item, info=OrderInfo()):
        item, info = str(item), str(info)
        if item == ALL:
            return len(self)
        elif info == ALL:
            return sum(self[item].values())
        else:
            return self[item][info]

    def __len__(self):
        return sum(sum(x.values()) for x in self.values())

    def clear(self):
        super().clear()

    def __str__(self):
        return f'Cart({len(self)})'
        return "Cart({nr_of_items})".format(nr_of_items=len(self))

    # def as_edit_form(self):
    #     return render_to_string('orders/cart_as_edit_form.html',
    #                             {'cart': self})

    def lines(self, user=None):
        if user and user.has_perm('client.user_is_client'):
            client = user.client
        else:
            client = None
        cart_lines = []
        # First index of cart dict is product_id, so this is
        # a loop over the first index.
        for product_id in self:
            item = models.OrderItem.objects.get(pk=product_id)
            # The info about a product is the second key to the cart
            # dict, so this for loops over all requested info.  I'm
            # using the current length of the cart line in this
            # enumerate to know the place off each line in the cart
            # when reordering.
            for line_nr, info_key in enumerate(self[product_id],
                                               len(cart_lines)):
                info = OrderInfo(info_key)
                delivery_id = info['delivery_event_id']
                if delivery_id is not None:
                    delivery = (
                        models.DeliveryDateForDeliveryAddress.objects.get(
                            pk=delivery_id))
                    assembly_point = delivery.delivery_address
                    delivery_date = delivery.start_date
                else:
                    assembly_point = delivery_date = None
                cart_lines.append({'cart_line_nr': line_nr,
                                   'product_id': product_id,
                                   'info_key': info_key,
                                   'number': self[product_id][info_key],
                                   'item': item,
                                   'info': info,
                                   'price': item.price(
                                       client, assembly_point, delivery_date),
                                   })
        return cart_lines

    def as_info_ordered_cart(
            self, info_key, to_name_sort_value=lambda x: (x, x)):

        return self._group_lines_by_info(
            self.lines(), info_key, to_name_sort_value)

    def as_info_ordered_form(
            self, info_key, to_name_sort_value=lambda x: (x, x)):

        return self._grouped_lines_as_form(self._group_lines_by_info(
            self.lines(), info_key, to_name_sort_value))

    @staticmethod
    def _group_lines_by_info(
            lines, info_key,
            to_name_sort_value=lambda x: (x, x)):
        """Returns the lines of the cart grouped.

        to_name_sort_value should should be a function that takes
        whatever the key returns from the info and returns a name to
        display and a value it can sort on.
        """
        if not lines:
            return []
        grouped_lines = []
        index_info_key_list = []
        for line in lines:
            info_item = line['info'][info_key]
            index_info_key_list.append(
                (line['cart_line_nr'], *to_name_sort_value(info_item)))
        index_info_key_list.sort(key=lambda x: x[2])
        title = index_info_key_list[0][1]
        title_list = []
        for line in index_info_key_list:
            if line[1] == title:
                title_list.append(lines[line[0]])
            else:
                grouped_lines.append(
                    (title, title_list))
                title = line[1]
                title_list = [lines[line[0]]]
        else:
            grouped_lines.append((title, title_list))
        return grouped_lines

    @staticmethod
    def _grouped_lines_as_form(grouped_lines):
        formdata = dict()
        for title, cartline_list in grouped_lines:
            title_form_data = []
            for cartline in cartline_list:
                title_form_data.append({
                    'number': cartline['number'],
                    'product_id': cartline['product_id'],
                    'product_description': cartline['item'].product.name,
                    'info_description': cartline['info']['special_requests'],
                    'price': cartline['price']})
            formdata[title] = forms.cart_table(initial=title_form_data,
                                               prefix=title,)
        return formdata

    @staticmethod
    def delivery_event_name_and_start_date(event_id):
        """Function to use with group_lines_by_info."""
        event = models.DeliveryDateForDeliveryAddress.objects.get(id=event_id)
        delivery_str = _('Delivery')
        title = (f'{event.safe_start_date} | '
                 f'{delivery_str} '
                 f'{event.delivery_address.address.address_name}')
        return (title,
                event.safe_start_datetime)

    def as_order(self, user=None,
                 category_function=None,
                 cart_info_function=None,
                 address_function=None,
                 delivery_date_function=None,
                 delivery_time_function=None,):
        """Returns the cart as an order.

        The category_function gets the cartline as input and you can
        extract whatever you want out of it.
        """
        category_str = category_function or (lambda x: '')
        cart_info_str = cart_info_function or (lambda x: str(x))
        to_address = address_function or (lambda x: None)
        to_delivery_date = delivery_date_function or (lambda x: None)
        to_delivery_time = delivery_time_function or (lambda x: None)
        user.client.order_set.filter(state=models.Order.NEW_ORDER).delete()
        order = models.Order()
        order.state = models.Order.NEW_ORDER
        order.client = user.client
        order.start_date = tz.now().date()
        order.start_time = tz.now().time()
        order.save()
        for cartline in self.lines(user=user):
            number = cartline['number']
            info = cartline['info']
            item = cartline['item']
            orderline = models.OrderLine()
            orderline.start_date = to_delivery_date(info)
            orderline.start_time = to_delivery_time(info)
            orderline.order = order
            orderline.category = category_str(cartline)
            orderline.number = number
            orderline.orderitem = item
            orderline.cart_info = cart_info_str(info)
            orderline.address = to_address(info)
            orderline.price = number * cartline['price']
            orderline.save()
            packing = item.product.packing
            if packing.deposit:
                deposit = models.Deposit()
                deposit.name = packing.name
                deposit.value = packing.deposit_value
                deposit.returned = False
                deposit.refunded = False
                deposit.order = order
                deposit.save()
        return order
