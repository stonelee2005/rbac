from django.shortcuts import render, HttpResponse, redirect, reverse
from myrbac import models
from myrbac.server.init_permission import init_permission
from django.conf import settings


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = models.User.objects.filter(name=username, password=password).first()

        err_msg = ''

        if not user:
            err_msg = '用户名或密码错误'
            return render(request, 'login.html', {'err_msg': err_msg})
        # 登陆成功
        # 将权限信息写入到session
        init_permission(request, user)

        return redirect(reverse('web:customer'))

    return render(request, 'login.html')
