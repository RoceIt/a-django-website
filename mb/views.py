from django.http import HttpResponse
from django.shortcuts import render

from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import permission_required


def index(request):
    '''A try'''
    mess = mark_safe("<h1> Dit kan beter</h1><p>Madame Bocal</p>")
    context = {
        # 'main': 'home',
        'homepage_message': mess,
    }
    return render(request, 'mb/index.html', context)


@permission_required('user.is_staff')
def staff_management(request):
    """Access to special spaces where staff members can access there
    management pages."""
    request_dict = {
        'check_menu_item': 'staff',
    }
    return render(request, 'mb/staff_management.html', request_dict)

def default_google_heath_check(request):
    """Pager requested by the google app engine health check service."""
    return HttpResponse('')
