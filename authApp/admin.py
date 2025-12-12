from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, About, Contact, ContactInfo, Plan, Tag, Blog
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    """Admin paneldə user yaratmaq üçün form"""
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_staff', 'is_active')

class CustomUserChangeForm(forms.ModelForm):
    """Admin paneldə user dəyişmək üçün form"""
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_staff', 'is_active')
        
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(ContactInfo)
admin.site.register(About)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Blog)