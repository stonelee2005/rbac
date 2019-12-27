from django.conf import settings

def init_permission(request,user):
    # #1.查当前登陆用户拥有的权限
    permission_query = user.roles.filter(permissions__url__isnull=False).values('permissions__url',
                                                                                'permissions__title',
                                                                                'permissions__menu_id',
                                                                                'permissions__menu__title',
                                                                                'permissions__menu__icon',
                                                                                ).distinct()

    # 存放权限信息
    # permission_list = []
    # menu_list = []
    #
    # for item in permission_query:
    #     permission_list.append({'url': item['permissions__url']})
    #
    #     if item.get('permissions__is_menu'):
    #         menu_list.append({'url': item['permissions__url'], 'icon': item['permissions__icon'],
    #                           'title': item['permissions__title']})

    # print(permission_list)
    # for i in permission_list:
    #     print(i)
    # #2.将权限信息写入的Session
    # request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # # #3.将菜单信息写入的Session
    # request.session[settings.MENU_SESSION_KEY] = menu_list



