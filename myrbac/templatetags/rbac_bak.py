import re

from django import template
from django.conf import settings
from collections import OrderedDict
register = template.Library()

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    #有序字典
    order_dict =OrderedDict()

    for i in sorted(menu_list,key=lambda x:menu_list[x]['weight'],reverse=True):
        order_dict[i] = menu_list[i]

    # print("order_dict.values :",order_dict.values())
    #实现页面打开是默认收起


    for item in order_dict.values():
        item['class'] = 'hide'

        for i in item['children']:

            if re.match('^{}$'.format(i['url']),request.path_info):
                i['class']= 'active'
                item['class'] = ''
    #         item['class']= 'active'

    return {"menu_list": order_dict}
