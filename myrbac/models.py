from django.db import models


# Create your models here.

class Menu(models.Model):
    """
    一级菜单
    """
    title =models.CharField(max_length=32,unique=True,verbose_name='菜单名')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    weight = models.IntegerField(default=1,verbose_name='顺序')
    class Meta:
        verbose_name_plural = "菜单表"
        verbose_name = "菜单表"

    def __str__(self):
        return '{}'.format(self.title)

class Permission(models.Model):
    """
    权限表
    有关联menu的二级菜单
    没有关联menu的不是二级菜单,是不可以做菜单
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=32, verbose_name='权限')
    # is_menu = models.BooleanField(default=False, verbose_name='是否菜单')
    # icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    menu = models.ForeignKey('Menu',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='菜单')
    parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.SET_NULL,verbose_name='上级菜单')
    name = models.CharField(max_length=32, blank=True,null=True,verbose_name='按钮权限',unique=True)
    class Meta:
        verbose_name_plural = "权限表"
        verbose_name = "权限表"

    def __str__(self):
        return '{}'.format(self.title)


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField(to='Role', verbose_name='用户所拥有的角色', blank=True, null=True)

    class Meta:
        verbose_name_plural = "用户表"
        verbose_name = "用户表"

    def __str__(self):
        return '{}|{}'.format(self.name, self.roles.all())


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所用的权限', blank=True, null=True)

    class Meta:
        verbose_name_plural = "角色表"
        verbose_name = "角色表"

    def __str__(self):
        return '{}|{}'.format(self.name, self.permissions.values_list())

