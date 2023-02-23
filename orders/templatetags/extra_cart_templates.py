from django import template
from django.urls import reverse
from django.utils.html import format_html

import orders.forms as forms
#from orders.forms import AddToCartForm, AddToCartWithDateInfo
from ..cart import ALL

register = template.Library()


@register.inclusion_tag('orders/add_to_cart.html')
def add_to_cart_form(product):
    prod_id = product.order.id

    return {'product': prod_id,
            'form': forms.AddToCartForm(initial={'product': prod_id}),
            'action_view': 'orders:add_to_cart'}


@register.inclusion_tag('orders/add_to_cart.html')
def add_to_cart_with_date_info_form(product):
    prod_id = product.order.id

    return {'product': prod_id,
            'form': forms.AddToCartWithDateInfo(initial={
                'product': prod_id}),
            'action_view': 'orders:add_to_cart_with_date_info'}


@register.inclusion_tag('orders/add_to_cart.html')
def add_to_cart_with_extra_requests_form(product):
    prod_id = product.order.id

    return {'product': prod_id,
            'form': forms.AddToCartWithExtraRequestsInfo(initial={
                'product': prod_id}),
            'action_view': 'orders:add_to_cart_with_extra_requests_info'}


@register.inclusion_tag('orders/add_to_cart.html')
def add_to_cart_with_event_info_form(product, client):
    prod_id = product.order.id

    return {
            'product': prod_id,
            'form': forms.AddToCartWithEventInfo(
                initial={'product': prod_id},
                choice_list=client.deliveries_choice_tuple()),
            'action_view': 'orders:add_to_cart_with_event_info'}


@register.inclusion_tag('orders/add_to_cart.html')
def add_to_cart_with_event_extra_requests_info_form(product, client):
    prod_id = product.order.id

    return {
            'product': prod_id,
            'form': forms.AddToCartWithEventExtraRequestsInfo(
                initial={'product': prod_id},
                choice_list=client.deliveries_choice_tuple()),
            'action_view': 'orders:add_to_cart_with_event_extra_requests_info'}


@register.simple_tag(takes_context=True)
def auto_updating_cart_item_counter(context):
    tag_template = '<span id="updating_cart_item_counter">{}</span>'
    try:
        nr_of_items = context.request.session['cart'].count(ALL)
    except KeyError:
        nr_of_items = 0

    return format_html(tag_template, nr_of_items)


@register.simple_tag
def edit_cart_txt(link_text='Check Cart/Order'):
    link = reverse('orders:edit_cart')
    tag_template = '<a href="{}">{}</a>'
    return format_html(tag_template, link, link_text)
