from django.contrib import admin

# Register your models here.
from myrbac import models

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title','url','menu','parent','name']
    list_editable = ['url','menu','name']
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(models.User)
admin.site.register(models.Menu)