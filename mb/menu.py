from django.shortcuts import render


def _render_in_x_tab(x):
    def render_it(request, template, dict_=None):
        request_dict = dict_ or dict()
        request_dict.update(check_menu_item=x)
        return render(request, template, request_dict)
    return render_it


render_without_tab = _render_in_x_tab(None)
render_in_info_tab = _render_in_x_tab('info')
render_in_staff_tab = _render_in_x_tab('staff')
