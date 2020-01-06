from django.db.models import Q
from django.forms import modelformset_factory, formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from myrbac import models
from myrbac.forms import RoleForm, MenuForm, PermissionForm, MultiPermissionForm


# Create your views here.
from myrbac.server.routes import get_all_url_dict


def role_list(request):
    all_roles = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {"all_roles": all_roles})


def role(request, edit_id=None):
    obj = models.Role.objects.filter(id=edit_id).first()
    form_obj = RoleForm(instance=obj)

    if request.method == "POST":
        form_obj = RoleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/form.html', {"form_obj": form_obj})


def del_role(request,del_id):
    models.Role.objects.filter(id =del_id).delete()
    return redirect(reverse('rbac:role_list'))


def menu_list(request):
    all_menu = models.Menu.objects.all()

    mid =request.GET.get('mid')

    if mid:
        permission_query = models.Permission.objects.filter(Q(parent__menu_id=mid)|Q(menu_id=mid))
    else:
        permission_query =models.Permission.objects.all()

    all_permission = permission_query.values('id', 'url', 'title', 'name', 'menu_id', 'parent_id', 'menu__title')

    all_permission_dict = {}

    for item in all_permission:
        menu_id = item.get('menu_id')

        if menu_id:
            item['children'] = []
            all_permission_dict[item['id']]=item

    for item in all_permission:

        pid = item.get('parent_id')

        if pid:
            all_permission_dict[pid]['children'].append(item)

    print(all_permission_dict)

    return render(request, 'rbac/menu_list.html', {"all_menu": all_menu,"all_permission_dict": all_permission_dict})


def menu(request, edit_id=None):
    obj = models.Menu.objects.filter(id=edit_id).first()
    form_obj = MenuForm(instance=obj)

    if request.method == "POST":
        form_obj = MenuForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/form.html', {"form_obj": form_obj})

def permission(request, edit_id=None):
    obj = models.Permission.objects.filter(id=edit_id).first()
    form_obj = PermissionForm(instance=obj)

    if request.method == "POST":
        form_obj = PermissionForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/form.html', {"form_obj": form_obj})

def del_permission(request,del_id):
    models.Permission.objects.filter(id =del_id).delete()
    return redirect(reverse('rbac:menu_list'))

def multi_permissions(request):
    # 批量操作
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    permissions = models.Permission.objects.all()

    # 获取路由系统中所有URL
    router_dict = get_all_url_dict()

    # 数据库中的所有权限的别名
    permissions_name_set = set([i.name for i in permissions])

    # 路由系统中的所有权限的别名
    router_name_set = set(router_dict.keys())

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            print(add_formset.cleaned_data)
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.name)

    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )