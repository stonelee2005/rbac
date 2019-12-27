from django.conf import settings

def init_permission(request,user):
    # #1.查当前登陆用户拥有的权限
    permission_query = user.roles.filter(permissions__url__isnull=False).values('permissions__url',
                                                                                'permissions__title',
                                                                                'permissions__id',
                                                                                'permissions__parent_id',
                                                                                'permissions__menu_id',
                                                                                'permissions__menu__title',
                                                                                'permissions__menu__icon',
                                                                                'permissions__menu__weight',
                                                                                ).distinct()

    # 存放权限信息
    permission_list = []

    # 存放菜单信息

    menu_dict = {}

    for item in permission_query:
        print('*'*10,item['permissions__id'])
        permission_list.append({'url': item['permissions__url'], 'id': item['permissions__id'],'pid': item['permissions__parent_id'],'title':item['permissions__title']})

        menu_id = item.get('permissions__menu_id')

        if not menu_id:
            continue

        if menu_id not in menu_dict:
            menu_dict[menu_id] = {


                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'weight': item['permissions__menu__weight'],
                'children': [
                    {'title': item['permissions__title'], 'url': item['permissions__url'],
                     'id': item['permissions__id'],'pid': item['permissions__parent_id']}
                ]
            }
        else:
            menu_dict[menu_id]['children'].append(
                {'title': item['permissions__title'], 'url': item['permissions__url'],
                  'id': item['permissions__id'], 'pid': item['permissions__parent_id']
                 })

    # print(menu_dict)
    # print("permission_list:",permission_list)
    # print(permission_list)
    # for i in permission_list:
    #     print(i)
    #2.将权限信息写入的Session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # #3.将菜单信息写入的Session
    request.session[settings.MENU_SESSION_KEY] = menu_dict



