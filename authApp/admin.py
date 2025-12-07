from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, About, Contact, ContactInfo, Plan

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'last_login', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number','active_test_count')}),
    )
    readonly_fields = ('last_login', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(ContactInfo)
admin.site.register(About)
admin.site.register(Plan)