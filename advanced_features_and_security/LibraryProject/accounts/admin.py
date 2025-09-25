from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for the admin interface.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'date_of_birth', 'profile_photo')


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form for the admin interface.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom user admin configuration.
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    # Fields to display in the user list
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Fields for the user detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )