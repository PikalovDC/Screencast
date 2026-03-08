from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


class CustomUserAdmin(UserAdmin):
    """Кастомная админка для модели User"""

    # Поля для отображения в списке пользователей
    list_display = ('email', 'username', 'phone_number', 'country', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)

    # Поля для просмотра и редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Персональная информация', {
            'fields': ('phone_number', 'country', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


# Регистрируем модель User с кастомной админкой
admin.site.register(User, CustomUserAdmin)


class GroupAdmin(admin.ModelAdmin):
    """Админка для групп"""
    list_display = ('name',)
    search_fields = ('name',)


# Регистрируем группы
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)