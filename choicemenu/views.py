from django.shortcuts import render
from django.urls import reverse

from .models import named_patterns_list
from .models import root_url_pattern


# Create your views here.
def full_url_conf(request):
    def structured_view(resolver, depth=0, structure=None):
        if structure == None:
            structure = []
        for pat in resolver:
            structure.append(depth*'________' + str(pat))
            if pat.__class__.__name__ == 'RegexURLResolver':
                structured_view(pat.url_patterns, depth+1, structure)
        return structure

    structure = structured_view(root_url_pattern())
    return render(request, 'choicemenu/full_url_conf.html', {'structure': structure} )

def top_menu(request):
    menu = [('home',reverse('mb_home')),
            ('url', reverse('named_patterns')),
            ('pi', reverse('personal_info')),
    ]
    return render(request, 'choicemenu/menu_list.html', {'menu': menu})
