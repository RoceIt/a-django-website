"""Site wide variables for use in patterns"""
from django.utils.translation import ugettext_lazy as _

def side_wide_vars(request):
    return  {
        'sw_add_item_icon': 'admin/img/icon-addlink.svg',
        'sw_change_item_icon': 'admin/img/icon-changelink.svg',
        'sw_delete_item_icon': 'admin/img/icon-deletelink.svg',
        'sw_add_item_title_attr_text': _('add'),
        'sw_change_item_title_attr_text': _('change'),
        'sw_delete_item_title_attr_text': _('delete'),
    }
