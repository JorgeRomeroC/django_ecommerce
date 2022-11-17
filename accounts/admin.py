from django.contrib import admin

from accounts.models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    # list_display = seran las propiedades que quiero que se muestren dentro de la vista tabla
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined','is_active')
    #cuando el usuario de click en una clumna este me lleve a su perfil
    list_display_links = ('email','first_name','last_name')
    #los campos de solo lectura seran las fecha en que se logeo por ultima vez y la fecha en la ques e unio a mi app
    readonly_fields = ('last_login','date_joined')
    #los usuarios seran ordenados segun la ultima fecha en que se unieron a mi app
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)
