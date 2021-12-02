from django.contrib import admin
from django.contrib.auth.models import Group, make_password
from django.contrib.auth.admin import UserAdmin
from .models import (
    Account,
    Student
)

admin.site.site_header = "Admin Panel"
admin.site.site_title = "AdminPanel"

# Register your models here.
admin.site.unregister(Group)


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ("username", "date_joined", "last_login", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("username",)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser'),
        })
    )


@admin.register(Student)
class StudentAdmin(AccountAdmin):
    list_filter = ("is_active", "date_joined")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': ('is_active',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=0)
