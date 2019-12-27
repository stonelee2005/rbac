import re

from django import template
from django.conf import settings
from collections import OrderedDict

register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    # 有序字典
    order_dict = OrderedDict()

    # print("order_dict.values :",order_dict.values())
    # 实现页面打开是默认收起

    for key in sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True):
        order_dict[key] = menu_list[key]
        item = order_dict[key]
        item['class'] = 'hide'

        for i in item['children']:
            print("i:" ,i)
            # if re.match('^{}$'.format(i['url']),request.path_info):
            if i['id'] == request.current_menu_id:
                i['class'] = 'active'
                item['class'] = ''
    #         item['class']= 'active'

    return {"menu_list": order_dict}

@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {"breadcrumb_list": request.breadcrumb_list}

@register.filter
def has_permission(request,permission):
    if permission in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True
