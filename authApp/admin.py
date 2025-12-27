from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, About, Contact, ContactInfo, Plan, Tag, Blog

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'last_login', 'date_joined','active_test_count')
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('phone_number','active_test_count')}),
    # )
    add_form_template = None
    def get_fieldsets(self, request, obj=None):
        if not obj: # Əgər yeni user yaradılırsa
            return (
                (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'active_test_count')}),
            )
        return super().get_fieldsets(request, obj)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'), # Yalnız email və şifrə
        }),
    )
    fieldsets = (
        ("General", {
            "fields": ("username", "password")
        }),
        ("Personal info", {
            "fields": ("first_name", "last_name", "email", "phone_number")
        }),
        ("Tests info", {
            "fields": ("active_test_count",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        }),)
    readonly_fields = ('last_login', 'date_joined','username')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(ContactInfo)
admin.site.register(About)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Blog)